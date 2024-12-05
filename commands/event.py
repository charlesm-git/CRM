import click
from sqlalchemy import select
from rich import print

from database import Session
from models.event import Event
from models.contract import Contract
from models.user import User
from views import eventview
from views import baseview
from utils.validation import email_validation, valid_token
from utils.permission import has_permission, has_object_permission


def valid_contract_selection(token, session, contract_id):
    contract = Contract.get_by_id(session, contract_id)
    if not contract:
        baseview.is_not_found_error()
        return False
    if contract.client.sales_contact_id != token["user_id"]:
        print(
            "[red]You can't assign an event to a client that is not your.[/red]"
        )
        return False
    if contract.contract_signed_status == False:
        print("[red]You can't assign an event to an unsigned contract.[/red]")
        return False
    if contract.event:
        print("[red]An event for this contract already exist[/red]")
        return False
    return True


@click.command(help="Create a new event")
def event_create():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-event"
            has_permission(permission, token)

            eventview.event_creation_welcome_message()

            while True:
                contract_id = eventview.get_contract_id()
                if valid_contract_selection(token, session, contract_id):
                    break

            data = eventview.event_creation()

            # Complementary data treatment
            data["contract_id"] = contract_id

            Event.create(session, **data)
            baseview.is_created()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(
    help="Update the support contact of an event selected from its ID"
)
@click.argument("id")
def event_update_support(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "update-support-event"
            has_permission(permission, token)

            event = Event.get_by_id(session, id)
            if not event:
                return baseview.is_not_found_error()

            baseview.display_object(event)

            eventview.event_update_support_contact_welcome_message()

            while True:
                support_contact_email = eventview.get_support_contact_email()
                if not email_validation(support_contact_email):
                    continue
                support_contact = User.get_from_email(
                    session, support_contact_email
                )
                if not support_contact:
                    baseview.is_not_found_error()
                    continue
                if support_contact.role.name != "support":
                    print("This user is not part of the support team.")
                else:
                    break

            event.update(session, support_contact_id=support_contact.id)
            baseview.is_updated()

    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Update a user selected from its ID")
@click.argument("id")
def event_update(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "update-event"

            event = Event.get_by_id(session, id)
            if not event:
                return baseview.is_not_found_error()

            has_object_permission(permission, token, event)

            baseview.display_object(event)

            new_data = eventview.event_update()

            while True:
                contract_id = eventview.get_contract_id()
                if contract_id == "":
                    break
                if valid_contract_selection(token, session, contract_id):
                    new_data["contract_id"] = contract_id
                    break

            event.update(session, **new_data)
            baseview.is_updated()

    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Delete a event selected from its ID")
@click.argument("id")
def event_delete(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "delete-event"

            event = Event.get_by_id(session, id)
            if not event:
                return baseview.is_not_found_error()

            has_object_permission(permission, token, event)

            event.delete(session)
            baseview.is_deleted()
    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Get the list all/your events")
@click.option(
    "--mine",
    is_flag=True,
    default=False,
    help="Shows your events only",
)
@click.option(
    "--no-support",
    is_flag=True,
    default=False,
    help="Shows events without support yet",
)
def event_list(mine, no_support):
    with Session() as session:
        token = valid_token()

        filters = []
        if mine:
            if token["role"] == "sales":
                filters.append(
                    Event.contract.has(
                        Contract.client.has(sales_contact_id=token["user_id"])
                    )
                )
            elif token["role"] == "support":
                filters.append(Event.support_contact_id == token["user_id"])
        if no_support:
            filters.append(Event.support_contact_id == None)

        events = session.scalars(select(Event).where(*filters)).all()

        if not events:
            print("No event fit these requirements")
        else:
            eventview.list_display(events)
