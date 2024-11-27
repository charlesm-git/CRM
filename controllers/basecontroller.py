from argon2 import PasswordHasher

from models.user import User


class BaseController:
    def __init__(self, view, session, authentication_controller):
        self.view = view
        self.session = session
        self.auth_controller = authentication_controller

    def user_creation(self, current_user):
        if not self.auth_controller.valid_token():
            return
        permission = "create-user"
        try:
            current_user.has_permission(permission)
            data = self.view.user_creation_view()
            hashed_password = self.hash_password(data["password"])
            User.create(
                self.session,
                name=data["name"],
                surname=data["surname"],
                email=data["email"],
                password=hashed_password,
                role_id=int(data["role"]),
            )
        except PermissionError as e:
            print(e)

    @staticmethod
    def hash_password(password):
        ph = PasswordHasher()
        return ph.hash(password)
