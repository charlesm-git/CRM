import click

from database import Session
from models.user import User
from views.userview import UserView
from utils.validation import valid_token, hash_password
from utils.permission import has_permission


@click.command(help="Create a new user")
def user_create():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-user"
            has_permission(permission, token)
            data = UserView.user_creation()
            hashed_password = hash_password(data["password"])
            User.create(
                session,
                name=data["name"],
                surname=data["surname"],
                email=data["email"],
                password=hashed_password,
                role_id=int(data["role_id"]),
            )
            UserView.user_created()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Update a user selected from its current email")
@click.argument("email")
def user_update(email):
    try:
        with Session() as session:
            token = valid_token()
            permission = "update-user"
            has_permission(permission, token)
            user_to_update = User.get_user_from_email(session, email)
            if not user_to_update:
                return UserView.user_not_found_error()
            new_data = UserView.user_update()
            user_to_update.update(session, **new_data)
            UserView.user_updated()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Delete a user selected from its email")
@click.argument("email")
def user_delete(email):
    try:
        with Session() as session:
            token = valid_token()
            permission = "delete-user"
            has_permission(permission, token)
            user_to_delete = User.get_user_from_email(session, email)
            if not user_to_delete:
                return UserView.user_not_found_error()
            user_to_delete.delete(session)
            UserView.user_deleted()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Get the list of all the users")
def user_list():
    with Session() as session:
        valid_token()
        users = User.get_all(session)
        for user in users:
            print(user)
