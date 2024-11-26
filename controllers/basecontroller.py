from argon2 import PasswordHasher

from models.user import User


class BaseController:
    def __init__(self, view, session):
        self.view = view
        self.session = session

    def user_creation(self, user):
        self.require_permission(user, "create-user")
        data = self.view.user_creation_view()
        hashed_password = self.hash_password(data["password"])
        user = User(
            name=data["name"],
            surname=data["surname"],
            email=data["email"],
            password=hashed_password,
            role_id=int(data["role"]),
        )
        user.save(self.session)
        
    @staticmethod
    def hash_password(password):
        ph = PasswordHasher()
        return ph.hash(password)
    
    @staticmethod
    def require_permission(user, action):
        if not user.has_permission(action):
            raise PermissionError(f"Permission denied for action : {action}")
    