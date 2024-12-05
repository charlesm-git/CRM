import click

from database import Session
from models.user import User
from views import userview
from views import baseview
from utils.validation import valid_token, hash_password
from utils.permission import has_permission


@click.command(help="Create a new user")
def user_create():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-user"
            has_permission(permission, token)

            # Get user input
            data = userview.user_creation()

            # Complementary data treatment
            data["password"] = hash_password(data["password"])

            User.create(session, **data)
            baseview.is_created()
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

            # Retrieve user to update
            user = User.get_from_email(session, email)
            if not user:
                return baseview.is_not_found_error()

            # Display a table containing the information retrieved
            baseview.display_object(user)

            # Get new input from user and update
            new_data = userview.user_update()
            user.update(session, **new_data)
            baseview.is_updated()
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

            # Retrieve user to delete
            user = User.get_from_email(session, email)
            if not user:
                return baseview.is_not_found_error()

            # Deletes it
            user.delete(session)
            baseview.is_deleted()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Get the list of all the users")
def user_list():
    with Session() as session:
        valid_token()
        # Retrieve all users
        users = User.get_all(session)
        # Display the users in a table
        userview.list_display(users)
