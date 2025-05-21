from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        # print("Before decoding token", flush=True)
        # print(f"Token: {token_data}", flush=True)
        
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    'error': "This token is invalid or has expired",
                    'resolution': "Please login again",
                }
            )
        
        if await token_in_blocklist(token_data["jti"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                'error': 'Token is invalid or has been revoked',
                'resolution': 'Please login again',
            })
        
        self.verify_token_data(token_data)
        return token_data
    def token_valid (self, token: str) -> bool:
        token_data = decode_token(token)
        # if token_data:
        #     return True
        # else:
        #     return False
        return token_data is not None
    def verify_token_data(self, token_data):
        raise NotImplementedError("please override this method in subclasses")
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid access token",
            )
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a valid refresh token",
            )