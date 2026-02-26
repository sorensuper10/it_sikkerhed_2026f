import requests

# --- Konfiguration --- #
AUTH_URL = "http://127.0.0.1:8000"
NOTES_URL = "http://127.0.0.1:8001"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin"

def test_get_token():
    """Hent token fra Auth-server"""
    response = requests.post(f"{AUTH_URL}/get_bearer_token", json={
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD
    })

    assert response.status_code == 200
    token = response.json().get("token")
    assert token is not None
    return token

def test_create_and_get_note():
    """Opret og hent note via Notes-service korrekt"""

    token = test_get_token()
    headers = {"token": token}

    # Send note som JSON
    payload = {"text": "Test note"}
    response_post = requests.post(f"{NOTES_URL}/notes", headers=headers, json=payload)

    print("Status code:", response_post.status_code)
    print("Response JSON:", response_post.json())

    assert response_post.status_code == 200, "Fejl ved oprettelse af note"

    note_id = response_post.json().get("note", {}).get("id")
    assert note_id is not None, "Ingen note ID returneret"

    # Hent noten
    response_get = requests.get(f"{NOTES_URL}/notes/{note_id}", headers=headers)
    assert response_get.status_code == 200, "Fejl ved hentning af note"
    assert response_get.json().get("note", {}).get("text") == "Test note"

def test_invalid_token():
    """Sørg for at forkert token giver 401"""
    headers = {"token": "Bearer invalidtoken123"}
    response = requests.get(f"{NOTES_URL}/notes", headers=headers)
    assert response.status_code == 401