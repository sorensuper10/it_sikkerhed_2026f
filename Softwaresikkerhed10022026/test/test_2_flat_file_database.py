import json
import os
import pytest

from Softwaresikkerhed10022026.flat_file.user import User
from Softwaresikkerhed10022026.flat_file.data_handler import Data_handler

pytestmark = pytest.mark.focus
test_file_name = "db_flat_file_test.json"


# ------------------------
# Helpers
# ------------------------
def create_json_file(filename: str, content: dict):
    """Helper til at oprette test-jsonfiler."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)


def delete_json_files():
    """Helper til at slette testfiler."""
    if os.path.exists(test_file_name):
        os.remove(test_file_name)


# ------------------------
# Setup / Cleanup for hver test
# ------------------------
@pytest.fixture(scope="function", autouse=True)
def cleanup_files():
    """Fjerner testfil før og efter hver test."""
    delete_json_files()  # Given: Start med tom database
    yield
    delete_json_files()  # Then: Ryd op efter test


# ------------------------
# Tests
# ------------------------

def test_create_and_find_user_success():
    """
    Test at en bruger kan oprettes og findes korrekt.
    RISIKO: Hvis denne test fejler, kan brugere ikke oprettes eller hentes.
    """
    # Given: Tom database
    data_handler = Data_handler(test_file_name)
    assert data_handler.get_number_of_users() == 0  # RISIKO: Hvis dette fejler, starter vi ikke fra tom database

    # When: Opret en bruger
    data_handler.create_user("John", "Doe", "Main Street", 10, "secret")

    # Then: Brugeren findes korrekt
    assert data_handler.get_number_of_users() == 1  # RISIKO: Hvis fejler, gemmes brugere ikke korrekt
    user: User = data_handler.get_user_by_id(0)
    assert user.first_name == "John"              # RISIKO: Forkert first_name kan indikere datakorruption
    assert user.last_name == "Doe"
    assert user.address == "Main Street"
    assert user.street_number == 10
    assert user.password == "secret"
    assert user.enabled is True                   # RISIKO: Bruger skal som standard være aktiv


def test_disable_and_enable_user():
    """
    Test at brugere kan deaktiveres og aktiveres korrekt.
    RISIKO: Hvis denne test fejler, håndteres brugerstatus ikke korrekt, hvilket kan påvirke sikkerhed.
    """
    # Given: To brugere er oprettet
    data_handler = Data_handler(test_file_name)
    data_handler.create_user("John", "Doe", "Main Street", 11, "secret")
    data_handler.create_user("John2", "Doe2", "Main Street2", 12, "secret2")
    assert data_handler.get_number_of_users() == 2
    user0: User = data_handler.get_user_by_id(0)
    user1: User = data_handler.get_user_by_id(1)
    assert user0.enabled is True
    assert user1.enabled is True

    # When: Deaktiver første bruger
    data_handler.disable_user(0)

    # Then: Første bruger skal være deaktiveret, anden stadig aktiv
    assert user0.enabled is False  # RISIKO: Hvis fejler, kan brugere fejlagtigt forblive aktive
    assert user1.enabled is True

    # When: Re-aktiver første bruger og deaktiver anden
    data_handler.disable_user(1)
    data_handler.enable_user(0)

    # Then: Status skal være korrekt
    assert user0.enabled is True
    assert user1.enabled is False  # RISIKO: Hvis fejler, håndteres status ikke korrekt