def login(username_exists, password_correct, account_locked, password_length):
    # Boundary / validation
    if password_length < 8 or password_length > 64:
        return False

    # Decision logic
    if not username_exists:
        return False
    if account_locked:
        return False
    if not password_correct:
        return False

    return True