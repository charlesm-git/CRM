from rich.console import Console
from rich.table import Table

from utils.validation import datetime_validation
from views import baseview


def event_creation_welcome_message():
    print("Enter the new event information.")


def get_contract_id():
    return input("Contract ID : ")


def event_creation():
    while True:
        name = input("Name : ")
        if name != "":
            break
        baseview.can_not_be_empty_error()

    while True:
        location = input("Location : ")
        if location != "":
            break
        baseview.can_not_be_empty_error()

    while True:
        attendees = input("Number of attendees : ")
        if attendees.isdigit():
            break
        baseview.can_not_be_empty_error()

    while True:
        start_date = input("Start date (format YYYY-MM-DD HH:MM): ")
        if datetime_validation(start_date):
            break
        baseview.invalid_format_error()

    while True:
        end_date = input("End date (format YYYY-MM-DD HH:MM): ")
        if datetime_validation(end_date):
            break
        baseview.invalid_format_error()

    note = input("Note (optional) : ")

    return {
        "name": name,
        "location": location,
        "attendees": attendees,
        "start_date": start_date,
        "end_date": end_date,
        "note": note,
    }


def event_update_support_contact_welcome_message():
    print(
        "Enter the email of the user that will be the support contact for this event"
    )


def get_support_contact_email():
    return input("Support contact email : ")


def event_update():
    baseview.update_message()

    name = input("Name : ")
    location = input("Location : ")

    while True:
        attendees = input("Number of attendees (number) : ")
        if attendees == "" or attendees.isdigit():
            break
        baseview.invalid_format_error()

    while True:
        start_date = input("Start date (format YYYY-MM-DD HH:MM): ")
        if start_date == "" or datetime_validation(start_date):
            break
        baseview.invalid_format_error()

    while True:
        end_date = input("End date (format YYYY-MM-DD HH:MM): ")
        if end_date == "" or datetime_validation(end_date):
            break
        baseview.invalid_format_error()

    note = input("Note (optional) : ")

    return {
        "name": name,
        "location": location,
        "attendees": attendees,
        "start_date": start_date,
        "end_date": end_date,
        "note": note,
    }


def list_display(events):
    console = Console()

    table = Table(
        title="Event List",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Event ID", width=5)
    table.add_column("Contract ID", width=8)
    table.add_column("Name")
    table.add_column("Client name")
    table.add_column("Client contact")
    table.add_column("Event start date", width=10)
    table.add_column("Event end date", width=10)
    table.add_column("Support contact")
    table.add_column("Location", min_width=20)
    table.add_column("Attendees")
    table.add_column("Note")

    for event in events:
        table.add_row(
            str(event.id),
            str(event.contract.id),
            event.name,
            f"{event.contract.client.name} {event.contract.client.surname}",
            f"{event.contract.client.email} {event.contract.client.phone_number}",
            str(event.start_date),
            str(event.end_date),
            f"{event.support_contact.name} {event.support_contact.surname}",
            event.location,
            str(event.attendees),
            event.note,
        )

    console.print(table)
