from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from src.config import Config
import jwt
import uuid
import logging
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE = 3600  # 1 hour

def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    return hash

def verify_password(password:str, hash:str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta = None, refresh: bool = False):
    payload = {
        "user": user_data,
        "exp": int((datetime.now(timezone.utc) + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRE))).timestamp()),
        "jti": str(uuid.uuid4()),
        "refresh": refresh,
    }
    print(f"Payload: {payload}", flush=True)
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )
    print(f"Generated Token: {token}", flush=True)
    print(f"Token Expiry (exp): {payload['exp']} (Unix Timestamp)", flush=True)
    print(f"Current UTC Time: {int(datetime.now(timezone.utc).timestamp())} (Unix Timestamp)", flush=True)
    return token
def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token, key=Config.JWT_SECRET, algorithms=[Config.JWT_ALGORITHM]
        )
        return token_data
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token has expired. Please log in again."
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Invalid token. Please provide a valid token."
        )


# def decode_token(token:str) -> dict:
#     try:
#         token_data = jwt.decode(
#             jwt = token,
#             key=Config.JWT_SECRET,
#             algorithms=[Config.JWT_ALGORITHM],
#         )
#         return token_data
#     except jwt.PyJWTError as e:
#         logging.error(f"JWT Error: {e}")
#         return None