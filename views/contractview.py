from rich.console import Console
from rich.table import Table

from views import baseview
from utils.validation import signed_status_validation


def contract_creation_welcome_message():
    print("Enter the new contract information.")


def get_client_id():
    return input("Client ID : ")


def contract_creation():
    while True:
        total_contract_amount = input(
            "Total amount of the contract (number only) : "
        )
        if total_contract_amount.isdigit():
            break
        baseview.invalid_format_error()

    while True:
        remaining_amount_to_pay = input(
            "Remaining amount to pay (Leave blank if nothing has been payed "
            "yet) : "
        )
        if remaining_amount_to_pay == "" or remaining_amount_to_pay.isdigit():
            break
        baseview.invalid_format_error()

    return {
        "total_contract_amount": total_contract_amount,
        "remaining_amount_to_pay": remaining_amount_to_pay,
    }


def contract_update():
    baseview.update_message()

    while True:
        total_contract_amount = input(
            "Total amount of the contract (number) : "
        )
        if total_contract_amount == "" or total_contract_amount.isdigit():
            break
        baseview.invalid_format_error()

    while True:
        remaining_amount_to_pay = input("Remaining amount to pay (number) : ")
        if remaining_amount_to_pay == "" or remaining_amount_to_pay.isdigit():
            break
        baseview.invalid_format_error()

    while True:
        contract_signed_status = input(
            "Contract signed status (0: unsigned / 1: signed) : "
        )
        if signed_status_validation(contract_signed_status):
            break
        baseview.invalid_format_error()

    return {
        "total_contract_amount": total_contract_amount,
        "remaining_amount_to_pay": remaining_amount_to_pay,
        "contract_signed_status": contract_signed_status,
    }


def list_display(contracts):
    """Display a list of Contract in a readable table"""
    console = Console()

    table = Table(
        title="Event List",
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("Contract ID", width=8)
    table.add_column("Client ID", width=6)
    table.add_column("Client name")
    table.add_column("Client contact")
    table.add_column("Sales contact")
    table.add_column("Total amount")
    table.add_column("Remaining to pay")
    table.add_column("Signed status")
    table.add_column("Creation Date")

    for contract in contracts:
        table.add_row(
            str(contract.id),
            str(contract.client.id),
            f"{contract.client.name} {contract.client.surname}",
            f"{contract.client.email} {contract.client.phone_number}",
            f"{contract.client.sales_contact.name} "
            f"{contract.client.sales_contact.surname}",
            str(contract.total_contract_amount),
            str(contract.remaining_amount_to_pay),
            str(contract.contract_signed_status),
            str(contract.date_created),
        )

    console.print(table)
