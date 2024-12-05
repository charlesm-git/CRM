from rich import print
from rich.console import Console
from rich.table import Table

from utils.validation import email_validation, phone_number_validation
from views import baseview


def client_creation():
    print("Enter the new client information.")

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
        phone_number = input("Phone number : ")
        if phone_number_validation(phone_number) and phone_number.split():
            break
        baseview.invalid_format_error()

    company = input("Company (optional) : ")

    return {
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone_number,
        "company": company,
    }


def client_update():
    baseview.update_message()
    name = input("Name : ")
    surname = input("Surname : ")

    while True:
        email = input("Email : ")
        if email == "" or email_validation(email):
            break
        baseview.invalid_format_error()

    while True:
        phone_number = input("Phone number : ")
        if phone_number == "" or (
            phone_number_validation(phone_number) and phone_number.split()
        ):
            break
        baseview.invalid_format_error()

    company = input("Company : ")

    return {
        "name": name,
        "surname": surname,
        "email": email,
        "phone_number": phone_number,
        "company": company,
    }
    
def client_update_sales_contact():
    return input("Sales contact email : ")


def client_already_exists_error():
    print(
        "[red]A client with this email already exists. Check the database.[/red]"
    )


def list_display(clients):
    console = Console()

    table = Table(
        title="Clients List",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("id")
    table.add_column("Name")
    table.add_column("Surname")
    table.add_column("Email")
    table.add_column("Phone Number")
    table.add_column("Company")
    table.add_column("Date created")
    table.add_column("Last update")
    table.add_column("Sales Contact")

    for client in clients:
        table.add_row(
            str(client.id),
            client.name,
            client.surname,
            client.email,
            client.phone_number,
            client.company,
            str(client.date_created),
            str(client.date_updated),
            f"{client.sales_contact.name} {client.sales_contact.surname}",
        )

    console.print(table)
