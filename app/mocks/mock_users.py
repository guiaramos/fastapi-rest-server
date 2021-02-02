from ..models.users import UserIn, UserSignIn


def get_mock_user():
    return UserIn(
        email="test@aaaa.com",
        password='banana',
        password_confirm='banana',
        name="test",
        display_name="test test",
        photo_url="http test",
        phone_number="01028969112"
    )


def get_mock_user_sign_in():
    return UserSignIn(
        email="test@aaaa.com",
        password='banana',
    )
