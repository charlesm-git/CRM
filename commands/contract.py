import click
from sqlalchemy import select

from database import Session
from models.contract import Contract
from models.client import Client
from views.contractview import ContractView
from utils.validation import signed_status_validation, valid_token
from utils.permission import has_permission, has_object_permission


@click.command(help="Create a new contract")
def contract_create():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-contract"
            has_permission(permission, token)

            ContractView.contract_creation_welcome_message()

            while True:
                client_id = ContractView.get_client_id()
                client = Client.get_by_id(session, client_id)
                if client:
                    break
                print(
                    "Client not found in the database. Check the ID given and try again."
                )

            data = ContractView.contract_creation()

            data["client_id"] = client_id

            if data["remaining_amount_to_pay"] == "":
                data["remaining_amount_to_pay"] = data["total_contract_amount"]

            Contract.create(session, **data)
            ContractView.contract_created()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Update a user selected from its ID")
@click.argument("id")
def contract_update(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "update-contract"

            contract_to_update = Contract.get_by_id(session, id)
            if not contract_to_update:
                return ContractView.contract_not_found_error()

            has_object_permission(permission, token, contract_to_update)

            new_data = ContractView.contract_update()

            if not signed_status_validation(
                new_data["contract_signed_status"]
            ):
                ContractView.signed_status_error()

            match new_data["contract_signed_status"]:
                case "0":
                    new_data["contract_signed_status"] = False
                case "1":
                    new_data["contract_signed_status"] = True
                case _:
                    new_data["contract_signed_status"] = ""

            contract_to_update.update(session, **new_data)
            ContractView.contract_updated()

    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Delete a contract selected from its ID")
@click.argument("id")
def contract_delete(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "delete-contract"

            contract_to_delete = Contract.get_by_id(session, id)
            if not contract_to_delete:
                return ContractView.contract_not_found_error()

            has_object_permission(permission, token, contract_to_delete)

            contract_to_delete.delete(session)
            ContractView.contract_deleted()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Get the list all/your contracts")
@click.option(
    "--mine",
    is_flag=True,
    default=False,
    help="Shows your clients contracts only",
)
@click.option(
    "--signed",
    is_flag=True,
    default=False,
    help="Shows the signed contracts only",
)
@click.option(
    "--unsigned",
    is_flag=True,
    default=False,
    help="Shows the unsigned contracts only",
)
@click.option(
    "--payed",
    is_flag=True,
    default=False,
    help="Show the fully payed contracts only",
)
@click.option(
    "--unpayed",
    is_flag=True,
    default=False,
    help="Show the non-fully payed contracts only",
)
def contract_list(mine, signed, unsigned, payed, unpayed):
    with Session() as session:
        token = valid_token()

        filters = []
        if mine:
            filters.append(
                Contract.client.has(sales_contact_id=token["user_id"])
            )
        if signed:
            filters.append(Contract.contract_signed_status == True)
        if unsigned:
            filters.append(Contract.contract_signed_status == False)
        if payed:
            filters.append(Contract.remaining_amount_to_pay == 0)
        if unpayed:
            filters.append(Contract.remaining_amount_to_pay != 0)

        contracts = session.scalars(select(Contract).where(*filters)).all()

        if not contracts:
            print("No contract fit these requirements")
        else:
            for contract in contracts:
                print(contract)
