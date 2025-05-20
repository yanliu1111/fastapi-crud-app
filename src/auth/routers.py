from fastapi import APIRouter, Depends
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status
from .utils import create_access_token, decode_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse
# from .dependencies import RefreshTokenBearer

auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRE = 2
@auth_router.post(
        "/signup",
        response_model=UserModel,
        status_code=status.HTTP_201_CREATED,)
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User already exists",
        )
    new_user = await user_service.create_user(user_data, session)
    
    return new_user

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
        raise HTTPException(
              status_code=status.HTTP_403_FORBIDDEN,
              detail="Invalid credentials",
          )

# @auth_router.get('/refresh-token')
# async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
#     token_data = decode_token(token_details)
#     if token_data:
#         new_access_token = create_access_token(user_data=token_data['user'])
#         return JSONResponse(
#             content={
#                 "message": "New access token generated",
#                 "access_token": new_access_token,
#             }
#         )
#     raise HTTPException(
#         status_code=status.HTTP_403_FORBIDDEN,
#         detail="Invalid or expired refresh token",
#     )