import click

from database import Session
from models.user import User
from models.client import Client
from views.clientview import ClientView
from utils.validation import valid_token, hash_password
from utils.permission import has_permission


@click.command(help="Create a new client")
def client_create():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-client"
            has_permission(permission, token)
            data = ClientView.client_creation()
            
            if data["company"] == "":
                data["company"] = None
            data["sales_contact_id"] = token["user_id"]
            
            Client.create(session, **data)
            ClientView.client_created()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Update a user selected from its ID")
@click.argument("id")
def client_update(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "update-client"
            has_permission(permission, token)
            client_to_update = Client.get_by_id(session, id)
            if not client_to_update:
                return ClientView.client_not_found_error()
            new_data = ClientView.client_update()
            client_to_update.update(session, **new_data)
            ClientView.client_updated()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Delete a client selected from its ID")
@click.argument("id")
def client_delete(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "delete-client"
            has_permission(permission, token)
            client_to_delete = Client.get_by_id(session, id)
            if not client_to_delete:
                return ClientView.client_not_found_error()
            client_to_delete.delete(session)
            ClientView.client_deleted()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Get the list all/your clients")
@click.option(
    "--mine", is_flag=True, default=False, help="Show your clients only"
)
def client_list(mine):
    with Session() as session:
        token = valid_token()
        if mine:
            clients = Client.get_from_sales_contact(session, token["user_id"])
        else:
            clients = Client.get_all(session)
            
        if not clients:
            return print("You do not have any client")
        
        for client in clients:
            print(client)
