from fastapi import APIRouter, Depends
from .schemas import UserCreateModel, UserLoginModel, UserBooksModel, EmailModel, PasswordResetRequestModel, PasswordResetConfirmModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from .utils import create_access_token, verify_password, create_url_safe_token, decode_url_safe_token, generate_password_hash
from datetime import timedelta, datetime
from fastapi.responses import JSONResponse
from .dependencies import RefreshTokenBearer, AccessTokenBearer, get_current_user, RoleChecker
from src.db.redis import add_jti_to_blocklist
from src.error import UserAlreadyExists, UserNotFound, InvalidCredentials, InvalidToken
from src.mail import mail, create_message
from src.config import Config
from src.db.main import get_session


auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(['admin', 'user'])

REFRESH_TOKEN_EXPIRE = 2

@auth_router.post('/send_mail')
async def send_mail(emails:EmailModel):
    emails = emails.addresses
    html = "<h1>Welcome to the app<h1>"
    message = create_message(
        recipients=emails,
        subject="Welcome to the app",
        body=html
    )
    await mail.send_message(message)
    return {"message": "Email sent successfully", "emails": emails}


@auth_router.post(
        "/signup",
        # response_model=UserModel,
        status_code=status.HTTP_201_CREATED,)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise UserAlreadyExists()
    
    new_user = await user_service.create_user(user_data, session)
    token = create_url_safe_token({
        "email": email,
    })
    link = f"http://{Config.DOMAIN}/api/v1/auth/verify/{token}" 
    html_message = f"""
    <h1>Welcome to the app, {new_user.email}!</h1>
    <p>Please click this <a href="{link}">Link</a> to verify your email.</p>
    <p>Thank you for joining us!</p>
    """
    message = create_message(
        recipients=[email],
        subject="Verify your email",
        body=html_message,
    )
    await mail.send_message(message)
    return {
        "message": "User created successfully. Please check your email to verify your account.",
        "user": {
            "email": new_user.email,
            "uid": str(new_user.uid),
        }
    }

@auth_router.get('/verify/{token}')
async def verify_user_account(token: str, session: AsyncSession = Depends(get_session)):

    token_data = decode_url_safe_token(token)
    email = token_data.get('email')
    
    if email:
        user = await user_service.get_user_by_email(email, session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user, {'is_verified': True}, session)
        return JSONResponse(
            content={
                "message": "Email verified successfully.",
                "user": {
                    "email": user.email,
                    "uid": str(user.uid),
                }
            },
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={
            "message": "Invalid or expired token.",
        },
        status_code=status.HTTP_400_BAD_REQUEST
    )


@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(user_data={
                'email': user.email,
                'user_uid': str(user.uid),
                'role': user.role,
            })
            refresh_token = create_access_token(user_data={
                'email': user.email,
                'user_uid': str(user.uid),
            }, expiry=timedelta(days = REFRESH_TOKEN_EXPIRE), refresh=True)

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )
        raise InvalidCredentials()

@auth_router.get('/refresh_token')
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    #    print(expiry_timestamp)
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(user_data=token_details['user'])
        return JSONResponse(
            content={
                "message": "New access token generated",
                "access_token": new_access_token,
            }
        )

    raise InvalidToken()

@auth_router.get('/me', response_model=UserBooksModel)
async def get_current_user(user = Depends(get_current_user), _:bool = Depends(role_checker)):
    return user

@auth_router.get('/logout')
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details.get("jti")
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message": "Logout successful",
        },
        status_code=status.HTTP_200_OK,
    )

@auth_router.post('/password-reset-request')
async def pass_reset_request(email_data: PasswordResetRequestModel, session: AsyncSession = Depends(get_session)):
    email = email_data.email
    user = await user_service.get_user_by_email(email, session)
    
    if not user:
        raise UserNotFound()
    
    token = create_url_safe_token({"email": email})
    link = f"http://{Config.DOMAIN}/api/v1/auth/password-reset-confirm/{token}"
    
    html_message = f"""
    <h1>Password Reset Request</h1>
    <p>Please click this <a href="{link}">Link</a> to reset your password.</p>
    """
    
    message = create_message(
        recipients=[email],
        subject="Password Reset Request",
        body=html_message,
    )
    
    await mail.send_message(message)
    
    return JSONResponse(
        content={
            "message": "Password reset link sent to your email.",
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post('/password-reset-confirm/{token}')
async def reset_account_password(token: str, password: PasswordResetConfirmModel, session: AsyncSession = Depends(get_session)):

    new_password = password.new_password
    confirm_password = password.confirm_new_password
    if not new_password or not confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password and confirmation are required."
        )

    token_data = decode_url_safe_token(token)
    email = token_data.get('email')
    
    if email:
        user = await user_service.get_user_by_email(email, session)
        if not user:
            raise UserNotFound()
        password_hash = generate_password_hash(new_password)
        await user_service.update_user(user, {'password_hash': password_hash}, session)
        return JSONResponse(
            content={
                "message": "Password Reset successfully.",
                "user": {
                    "email": user.email,
                    "uid": str(user.uid),
                }
            },
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={
            "message": "Error happened while resetting password. Please try again later.",
        },
        status_code=status.HTTP_400_BAD_REQUEST
    )