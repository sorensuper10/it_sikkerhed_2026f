import pytest

def test_pass_with_variables():
    # Passerer
    number1 = 10
    number2 = 5
    result = number1 + number2

    assert result == 15


def test_fail_with_variables():
    # Fejler (forkert forventet resultat)
    number1 = 10
    number2 = 5
    result = number1 - number2

    assert result == 10


def test_crash_with_variables():
    # Crasher (division med nul)
    number1 = 10
    number2 = 0
    result = number1 / number2

@pytest.mark.skip(reason="Springes over med vilje")
def test_skip_with_variables():
    number1 = 10
    number2 = 5
    assert number1 * number2 == 50