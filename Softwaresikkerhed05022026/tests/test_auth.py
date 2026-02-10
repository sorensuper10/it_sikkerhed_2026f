import pytest
from auth import login

@pytest.mark.parametrize(
    "username_exists, password_correct, account_locked, password_length, expected",
    [
        # username | password | locked | length | result
        (True,  True,  False, 8,   True),   # Gyldigt login (nedre grænse)
        (True,  True,  False, 64,  True),   # Gyldigt login (øvre grænse)

        (True,  False, False, 12,  False),  # Forkert password
        (False, True,  False, 12,  False),  # Brugernavn findes ikke
        (True,  True,  True,  12,  False),  # Konto låst

        (True,  True,  False, 7,   False),  # Under grænse (boundary)
        (True,  True,  False, 65,  False),  # Over grænse (boundary)
    ]
)
def test_login_decision_table(
    username_exists,
    password_correct,
    account_locked,
    password_length,
    expected
):
    assert login(
        username_exists,
        password_correct,
        account_locked,
        password_length
    ) is expected

@pytest.mark.parametrize(
    "password_length, expected",
    [
        (7, False),
        (8, True),
        (9, True),
        (64, True),
        (65, False),
    ]
)
def test_password_length_boundaries(password_length, expected):
    assert login(True, True, False, password_length) is expected

@pytest.mark.parametrize(
    "password_length",
    [8, 12, 32, 64]
)
def test_valid_password_lengths(password_length):
    assert login(True, True, False, password_length) is True