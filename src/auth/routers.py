from fastapi import APIRouter

auth_router = APIRouter()

@auth_router.post("/signup")
async def create_user_account():
    return {"message": "User signed up successfully"}