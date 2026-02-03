import pytest

def test_pass():
    # Denne test vil passere
    assert 1 + 1 == 2


def test_fail():
    # Denne test vil fejle
    assert 1 * 1 == 3

@pytest.mark.skip(reason="Springes over med vilje") # Denne test bliver slet ikke kørt
def test_skip():
    assert False # failed test bliver ignoreret
    raise RuntimeError("Test crashede med vilje") # crash bliver også ignoreret


def test_crash():
    # Denne test crasher med en exception
    raise RuntimeError("Test crashede med vilje")
    assert False # failed test bliver ignoreret

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