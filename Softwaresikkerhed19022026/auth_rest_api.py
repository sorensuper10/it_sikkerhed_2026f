import json
from fastapi import FastAPI, Depends, HTTPException, Header, Body
from typing import List

from Softwaresikkerhed19022026.user_service import User_service
from Softwaresikkerhed19022026.models import User, Role
from Softwaresikkerhed19022026.auth_rest_api_models import RegisterUserRequest, GetBearerTokenRequest, ActivateUserRequest
from pydantic import BaseModel
from typing import List
from Softwaresikkerhed19022026.models import Role
from Softwaresikkerhed19022026.auth_rest_api_models import (
    RegisterUserRequest,
    GetBearerTokenRequest,
    ActivateUserRequest,
    UpdateUserRequest
)

class Auth_rest_api:

    def __init__(self, database_file: str = "db_user_flat_file.json"):
        self.user_service = User_service(database_file)

        self.app = FastAPI()
        #self.app.add_event_handler("startup", self.on_startup)

        self.app.post("/register_user")(self.register_user)
        self.app.post("/get_bearer_token")(self.get_bearer_token)
        self.app.post("/deactivate_user")(self.deactivate_user)
        self.app.post("/activate_user")(self.activate_user)
        self.app.get("/users/{username}")(self.get_user)
        self.app.put("/users/{username}")(self.update_user)
        self.app.delete("/users/{username}")(self.delete_user)
        self.app.get("/users")(self.list_users)

    def get_user(self, username: str, token: str = Header(...)):

            if not token.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

            user = self.user_service.get_user(token, username)

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return user

    def update_user(
            self,
            username: str,
            post_variables: UpdateUserRequest,
            token: str = Header(...)
    ):

        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        self.user_service.update_user(
            token,
            username,
            post_variables.first_name,
            post_variables.last_name,
            post_variables.roles
        )

        return {"status": f"user '{username}' updated"}

    def delete_user(self, username: str, token: str = Header(...)):

        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        self.user_service.delete_user(token, username)

        return {"status": f"user '{username}' deleted"}

    def list_users(self, token: str = Header(...)):

        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        return self.user_service.get_all_users(token)

    def register_user(self, post_variables: RegisterUserRequest):
        self.user_service.register_user(
            post_variables.username, 
            post_variables.password, 
            post_variables.first_name, 
            post_variables.last_name, 
            post_variables.roles
        )
        return { "status": "user created"}

    def get_bearer_token(self, post_variables: GetBearerTokenRequest):
        token = self.user_service.get_bearer_token(post_variables.username, post_variables.password)
        return {"token": token}

    def deactivate_user(
            self, 
            post_variables: ActivateUserRequest,
            token: str = Header(...)
        ):

        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

        self.user_service.deactivate_user(token, post_variables.username)
        return { "status": f"user '{post_variables.username}' has been deactivated"}

    def activate_user(
            self, 
            post_variables: ActivateUserRequest,
            token: str = Header(...)
        ):
        if not token.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")
        
        self.user_service.activate_user(token, post_variables.username)
        return { "status": f"user '{post_variables.username}' has been reactivated"}
