from argon2 import PasswordHasher
import click
from database import Session

from models.user import User
from views.userview import UserView
from utils.validation import valid_token, hash_password
from utils.permission import has_permission

@click.command(help="Create a new CRM user")
def user_creation():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-user"
            has_permission(permission, token)
            data = UserView.user_creation_view()
            hashed_password = hash_password(data["password"])
            User.create(
                session,
                name=data["name"],
                surname=data["surname"],
                email=data["email"],
                password=hashed_password,
                role_id=int(data["role"]),
            )
            UserView.user_created()
    except PermissionError as e:
        raise click.ClickException(e)


