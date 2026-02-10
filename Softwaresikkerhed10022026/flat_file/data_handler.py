from Softwaresikkerhed10022026.flat_file.user import User
from Softwaresikkerhed10022026.flat_file.flat_file_loader import Flat_file_loader

class Data_handler:
    def __init__(self, flat_file_name="users.json"):
        self.flat_file_loader = Flat_file_loader(flat_file_name)
        # load_memory_database_from_file returnerer dict[str, User]
        self.users: dict[int, User] = self.flat_file_loader.load_memory_database_from_file()

    def get_number_of_users(self):
        return len(self.users)

    def get_user_by_id(self, user_id: int):
        return self.users.get(user_id)

    def create_user(self, first_name, last_name, address, street_number, password):
        user_id = len(self.users)
        enabled = True
        user = User(user_id, first_name, last_name, address, street_number, password, enabled)
        self.users[user_id] = user
        self.flat_file_loader.save_memory_database_to_file(self.users)

    def disable_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.enabled = False
            self.flat_file_loader.save_memory_database_to_file(self.users)

    def enable_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            user.enabled = True
            self.flat_file_loader.save_memory_database_to_file(self.users)

    # -------------------
    # Update metoder
    # -------------------
    def update_first_name(self, user_id, new_first_name):
        user = self.get_user_by_id(user_id)
        if user:
            user.first_name = new_first_name
            self.flat_file_loader.save_memory_database_to_file(self.users)

    def update_last_name(self, user_id, new_last_name):
        user = self.get_user_by_id(user_id)
        if user:
            user.last_name = new_last_name
            self.flat_file_loader.save_memory_database_to_file(self.users)

    def update_address(self, user_id, new_address):
        user = self.get_user_by_id(user_id)
        if user:
            user.address = new_address
            self.flat_file_loader.save_memory_database_to_file(self.users)

    def update_street_number(self, user_id, new_street_number):
        user = self.get_user_by_id(user_id)
        if user:
            user.street_number = new_street_number
            self.flat_file_loader.save_memory_database_to_file(self.users)

    def update_password(self, user_id, new_password):
        user = self.get_user_by_id(user_id)
        if user:
            user.password = new_password
            self.flat_file_loader.save_memory_database_to_file(self.users)