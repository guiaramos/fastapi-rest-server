from .users import check_confirm_password, get_password_hash


def test_check_confirm_password():
    # test if the confirm password returns true when the passwords are correct
    password = 'banana'
    password_confirm = 'banana'
    is_same = check_confirm_password(password, password_confirm)
    assert is_same


def test_check_confirm_wrong_password():
    # test if the confirm password returns false when the passwords are incorrect
    password = 'pizza'
    password_confirm = 'banana'
    is_same = check_confirm_password(password, password_confirm)
    assert not is_same


def test_get_password_hash():
    # test if function hashes the password
    password = 'pizza'
    hashed_password = get_password_hash(password)
    assert password != hashed_password
