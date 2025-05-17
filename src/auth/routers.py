from fastapi import APIRouter, Depends
from .schemas import UserCreateModel
from .service import UserService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession

auth_router = APIRouter()
user_service = UserService()
@auth_router.post("/signup")
async def create_user_account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
):
    
    email = user_data.email
    user_exists = user_service.user_exists(email, session)