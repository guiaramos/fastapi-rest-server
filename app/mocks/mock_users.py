from ..models.users import UserIn


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
