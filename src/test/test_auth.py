from src.auth.schemas import UserCreateModel
auth_prefix = f"/api/v1/auth"
def test_user_createion(fake_session, fake_user_service, test_client):
    signup_data = {
            "first_name":"LuLu",
            "last_name":"LiuLiu",
            "email": "testemailaccount@gmail.com",
            "username": "lulu123",
            "password":"test12345"
          }
    response = test_client.post(
        url=f"{auth_prefix}/signup",
        json= signup_data,
    )
    user_data = UserCreateModel(**signup_data)
    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(signup_data['email'],fake_session)
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(user_data, fake_session)