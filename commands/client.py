import click

from database import Session
from models.client import Client
from models.user import User
from views import clientview
from views import baseview
from utils.validation import valid_token
from utils.permission import has_permission, has_object_permission


@click.command(help="Create a new client")
def client_create():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-client"
            has_permission(permission, token)

            # Get client data from user
            data = clientview.client_creation()

            # Check if there is already a client with this email in the DB
            # (has to be unique)
            if Client.get_from_email(session, data["email"]):
                return clientview.client_already_exists_error()

            # Complementary data treatment
            if data["company"] == "":
                data["company"] = None
            data["sales_contact_id"] = token["user_id"]

            Client.create(session, **data)
            baseview.is_created()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Update a user selected from its ID")
@click.argument("id")
def client_update(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "update-client"

            # Retrieve client to update
            client = Client.get_by_id(session, id)
            if not client:
                return baseview.is_not_found_error()

            # Check the object permission
            has_object_permission(permission, token, client)

            # Display the information of the client that is being updated in
            # a table
            baseview.display_object(client)

            # Get new data from user
            new_data = clientview.client_update()

            # Verification that the sales_contact_id provided is valid
            while True:
                sales_contact_email = clientview.client_update_sales_contact()
                if sales_contact_email == "":
                    break
                sales_contact = User.get_from_email(
                    session, sales_contact_email
                )
                # User has to exist
                if not sales_contact:
                    baseview.is_not_found_error()
                    continue
                # User has to be from the sales departement
                if sales_contact.role.name != "sales":
                    print("This user is not part of the sales team.")
                    continue
                new_data["sales_contact_id"] = sales_contact.id
                break

            client.update(session, **new_data)
            baseview.is_updated()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Delete a client selected from its ID")
@click.argument("id")
def client_delete(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "delete-client"

            # Retrieve client to delete
            client = Client.get_by_id(session, id)
            if not client:
                return baseview.is_not_found_error()

            # Check object permission
            has_object_permission(permission, token, client)

            client.delete(session)
            baseview.is_deleted()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Get the list all/your clients")
@click.option(
    "--mine", is_flag=True, default=False, help="Show your clients only"
)
def client_list(mine):
    """
    Display a list of the clients as a table

    no filter : all clients in the DB are displayed
    --mine filter : Only the clients of the logged in user are displayed
    """
    with Session() as session:
        token = valid_token()
        if mine:
            clients = Client.get_from_sales_contact(session, token["user_id"])
        else:
            clients = Client.get_all(session)

        if not clients:
            print("You do not have any client")
        else:
            clientview.list_display(clients)
