from fastapi.security import HTTPBearer
from fastapi import Request, status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import Any, List
from src.error import (InvalidToken, InsufficientPermission, AccessTokenRequired, RefreshTokenRequired, AccountNotVerified)
from src.db.models import User

user_service = UserService()
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
            raise InvalidToken()
        
        if await token_in_blocklist(token_data["jti"]):
            raise InvalidToken()
        
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
            raise AccessTokenRequired()
        
class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data["refresh"]:
            raise RefreshTokenRequired()

async def get_current_user(token_details: dict = Depends(AccessTokenBearer()), 
                     session: AsyncSession = Depends(get_session)):
    user_email = token_details["user"]["email"]
    user = await user_service.get_user_by_email(user_email, session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles: List[str])-> None:
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User=Depends(get_current_user))-> Any:
        if not current_user.is_verified:
            raise AccountNotVerified()
        if current_user.role not in self.allowed_roles:
            raise InsufficientPermission()
        return current_user
            