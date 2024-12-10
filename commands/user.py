import click
from rich import print
from sentry_sdk import capture_message
from sqlalchemy.exc import IntegrityError

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

            # Create the user in the database
            user = User.create(session, **data)
            baseview.is_created()

            # Sentry Logs
            message = (
                f"New User (id {user.id}) created by User {token["user_id"]}\n"
                f"ID : {user.id}\n"
                f"Name : {user.name} {user.surname}\n"
                f"Email : {user.email}\n"
                f"Role : {user.role.name}\n"
            )
            capture_message(
                message,
                fingerprint=[f"user-create-{user.id}-{token['user_id']}"],
            )
    except PermissionError as e:
        raise click.ClickException(e)
    except IntegrityError:
        print(
            "[red]The email you provided is already used for another account. "
            "Try again.[/red]"
        )
        raise click.ClickException("Sorry, something went wrong.")


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

            # Stores old user data for Sentry logs
            old_data = {
                attr: getattr(user, attr)
                for attr in user.__table__.columns.keys()
            }

            # Get new input from user and update
            new_data = userview.user_update()
            user.update(session, **new_data)
            baseview.is_updated()

            # Sentry Logs
            message = (
                f"User {user.id} updated by User {token['user_id']}\n"
                f"Old value --> New value\n"
            )
            for key, value in new_data.items():
                if value == "":
                    continue
                if key == "password":
                    message += "Password --> Modified\n"
                    continue
                message += (
                    f"{key} : {old_data.get(key)} --> {new_data.get(key)}\n"
                )
            capture_message(
                message,
                fingerprint=[f"user-update-{user.id}-{token['user_id']}"],
            )
    except PermissionError as e:
        raise click.ClickException(e)
    except IntegrityError:
        print(
            "[red]The email you provided is already used for another account. "
            "All changes have been discarded. Try again.[/red]"
        )
        raise click.ClickException("Sorry, something went wrong.")


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

            # Sentry Log
            capture_message(
                f"User {user.id} deleted by User {token["user_id"]}",
                fingerprint=[f"user-delete-{user.id}"],
            )
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
