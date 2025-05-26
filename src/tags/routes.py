from fastapi import APIRouter, Depends, status
from .service import TagService
from src.auth.dependencies import RoleChecker
from src.db.main import get_session
from .schemas import TagModel, TagCreateModel, TagUpdateModel

tags_router = APIRouter()
tag_service = TagService()
user_role_checker = Depends(RoleChecker(["admin", "user"]))