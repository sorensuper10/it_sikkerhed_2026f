import json
from dataclasses import asdict
from Softwaresikkerhed10022026.flat_file.user import User
from cryptography.fernet import Fernet
import bcrypt
import os

# Hent krypteringsnøglen fra environment
key = os.environ.get("ENCRYPTION_KEY")
if not key:
    print("WARNING: ENCRYPTION_KEY not found! Generating temporary key for testing.")
    key = Fernet.generate_key()
fernet = Fernet(key)

class Flat_file_loader:
    def __init__(self, database_file_name: str = "db_flat_file.json"):
        # Sørg for, at filstien altid peger på projektets src-mappe
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # én mappe op fra flat_file
        self.database_file_name = os.path.join(base_dir, database_file_name)

        # Sørg for at mappen eksisterer
        os.makedirs(os.path.dirname(self.database_file_name), exist_ok=True)

    def load_memory_database_from_file(self) -> dict:
        in_memory_database = {}
        try:
            with open(self.database_file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                for user_dict in data.get("users", []):
                    # Dekrypter alle personfølsomme felter
                    for field in ["first_name", "last_name", "address", "street_number"]:
                        user_dict[field] = fernet.decrypt(user_dict[field].encode()).decode()
                    # Password forbliver hashed
                    user = User(**user_dict)
                    in_memory_database[str(user.person_id)] = user
        except FileNotFoundError:
            print(f"WARNING: file '{self.database_file_name}' don't exist. Starter med tom database.")
        except json.JSONDecodeError:
            print(f"WARNING: file '{self.database_file_name}' er korrupt. Starter med tom database.")
        return in_memory_database

    def save_memory_database_to_file(self, in_memory_database: dict):
        serializable_db = {"users": []}
        for user in in_memory_database.values():
            user_dict = asdict(user)
            # Krypter personfølsomme felter
            for field in ["first_name", "last_name", "address", "street_number"]:
                user_dict[field] = fernet.encrypt(user_dict[field].encode()).decode()
            # Hash password
            user_dict["password"] = bcrypt.hashpw(user_dict["password"].encode(), bcrypt.gensalt()).decode()
            serializable_db["users"].append(user_dict)
        with open(self.database_file_name, "w", encoding="utf-8") as f:
            json.dump(serializable_db, f, indent=2, ensure_ascii=False)