from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import status
from fastapi.responses import RedirectResponse
from Softwaresikkerhed10022026.flat_file.flat_file_loader import Flat_file_loader
from Softwaresikkerhed10022026.flat_file.user import User
import os

class Rest_api:
    def __init__(self, database_file_name: str = "./db_flat_file.json", templates_dir: str = None):
        self.flat_file_loader = Flat_file_loader(database_file_name)
        self.in_memory_database: dict[str, User] = {}

        self.app = FastAPI()

        # Brug den angivne template-mappe, eller default
        templates_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.templates = Jinja2Templates(directory=templates_dir)

        self.app.add_event_handler("startup", self.on_startup)

        # Routes
        self.app.get("/", response_class=HTMLResponse)(self.root)
        self.app.post("/person")(self.create_person)
        self.app.get("/get_person", response_class=HTMLResponse)(self.get_person_form)
        self.app.get("/person/{person_id}")(self.read_person)

    def on_startup(self):
        self.in_memory_database = self.flat_file_loader.load_memory_database_from_file()

    # Forside: viser alle brugere og success-message hvis relevant
    def root(self, request: Request, message: str = None):
        users = list(self.in_memory_database.values())
        return self.templates.TemplateResponse(
            "index.html",
            {"request": request, "users": users, "message": message}
        )

    # Opret bruger
    def create_person(
        self,
        request: Request,
        person_id: int = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        address: str = Form(...),
        street_number: str = Form(...),
        password: str = Form(...),
        enabled: str = Form(None)  # Checkbox
    ):
        is_enabled = enabled == "true"
        user = User(person_id, first_name, last_name, address, street_number, password, is_enabled)
        self.in_memory_database[str(person_id)] = user
        self.flat_file_loader.save_memory_database_to_file(self.in_memory_database)
        message = f"User {first_name} {last_name} gemt!"
        return RedirectResponse(url=f"/?message={message}", status_code=status.HTTP_303_SEE_OTHER)

    # Hent én bruger via formular
    def get_person_form(self, request: Request, person_id: int):
        person = self.in_memory_database.get(str(person_id))
        users = list(self.in_memory_database.values())  # Tilføj alle brugere
        return self.templates.TemplateResponse(
            "index.html",
            {"request": request, "person": person, "users": users}  # send både person og users
        )

    # Hent én bruger via API
    def read_person(self, person_id: int):
        person = self.in_memory_database.get(str(person_id))
        if not person:
            raise HTTPException(status_code=404, detail=f"User med id '{person_id}' findes ikke")
        return person


# Initialiser API
api = Rest_api(database_file_name="./src/db_flat_file.json")
app = api.app