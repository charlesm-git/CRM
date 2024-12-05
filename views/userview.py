from rich.console import Console
from rich.table import Table

from utils.validation import email_validation, role_validation
from views import baseview


def user_creation():
    print("Enter the new user information.")

    while True:
        name = input("Name : ")
        if name != "":
            break
        baseview.can_not_be_empty_error()

    while True:
        surname = input("Surname : ")
        if surname != "":
            break
        baseview.can_not_be_empty_error()

    while True:
        email = input("Email : ")
        if email_validation(email):
            break
        baseview.invalid_format_error()

    while True:
        password = input("Password : ")
        if password != "":
            break
        baseview.can_not_be_empty_error()

    while True:
        role_id = input("Role (1: sales / 2: management / 3: support) : ")
        if role_validation(role_id):
            break
        baseview.invalid_format_error()

    return {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password,
        "role_id": role_id,
    }


def user_update():
    baseview.update_message()
    name = input("Name : ")
    surname = input("Surname : ")

    while True:
        email = input("Email : ")
        if email == "" or email_validation(email):
            break
        baseview.invalid_format_error()

    password = input("Password : ")

    while True:
        role_id = input("Role (1: sales / 2: management / 3: support) : ")
        if role_id == "" or role_validation(role_id):
            break
        baseview.invalid_format_error()

    return {
        "name": name,
        "surname": surname,
        "email": email,
        "password": password,
        "role_id": role_id,
    }


def list_display(users):
    console = Console()

    table = Table(
        title="Users List",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("id")
    table.add_column("Name")
    table.add_column("Surname")
    table.add_column("Email")
    table.add_column("Role")
    table.add_column("Date created")
    table.add_column("Last update")

    for user in users:
        table.add_row(
            str(user.id),
            user.name,
            user.surname,
            user.email,
            user.role.name,
            str(user.date_created),
            str(user.date_updated),
        )

    console.print(table)
