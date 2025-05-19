from fastapi.security import HTTPBearer
from fastapi import Request, status
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        # print(creds.scheme)
        # print(creds.credentials)
        token = creds.credentials
        from fastapi.security.http import HTTPAuthorizationCredentials
from fastapi.exceptions import HTTPException
from fastapi import status, Request
from fastapi.security import HTTPBearer

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)
        # print("Before decoding token", flush=True)
        # print(f"Token: {token_data}", flush=True)
        
        if token_data:
            return token_data
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token",
            )

        
    def token_valid (self, token: str) -> bool:
        token_data = decode_token(token)
        if token_data:
            return True
        else:
            return False