import click
from sqlalchemy import select

from database import Session
from models.event import Event
from models.contract import Contract
from models.user import User
from views.eventview import EventView
from utils.validation import (
    email_validation,
    signed_status_validation,
    valid_token,
)
from utils.permission import has_permission, has_object_permission


@click.command(help="Create a new event")
def event_create():
    try:
        with Session() as session:
            token = valid_token()
            permission = "create-event"
            has_permission(permission, token)

            EventView.event_creation_welcome_message()

            while True:
                contract_id = EventView.get_contract_id()
                contract = Contract.get_by_id(session, contract_id)
                if not contract:
                    print(
                        "Contract not found in the database. Check the ID given and try again."
                    )
                    continue
                if contract.client.sales_contact_id != token["user_id"]:
                    print(
                        "You can't create an event for a client that is not your."
                    )
                    continue
                if contract.contract_signed_status == False:
                    print(
                        "You can't create an event for an unsigned contract."
                    )
                    continue
                break

            data = EventView.event_creation()

            data["contract_id"] = contract_id

            Event.create(session, **data)
            EventView.event_created()
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

            event_to_update = Event.get_by_id(session, id)
            if not event_to_update:
                return EventView.event_not_found_error()

            EventView.event_update_support_contact_welcome_message()

            while True:
                support_contact_email = EventView.get_support_contact_email()
                if not email_validation(support_contact_email):
                    continue
                support_contact = User.get_from_email(
                    session, support_contact_email
                )
                if not support_contact:
                    print(
                        "User not found in the database. Check the email and try again."
                    )
                    continue
                if support_contact.role.name != "support":
                    print("This user is not part of the support team.")
                else:
                    break

            event_to_update.update(
                session, support_contact_id=support_contact.id
            )
            EventView.event_updated()

    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Update a user selected from its ID")
@click.argument("id")
def event_update(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "update-event"

            event_to_update = Event.get_by_id(session, id)
            if not event_to_update:
                return EventView.event_not_found_error()

            has_object_permission(permission, token, event_to_update)

            new_data = EventView.event_update()

            event_to_update.update(session, **new_data)
            EventView.event_updated()

    except PermissionError as e:
        raise click.ClickException(e)


@click.command(help="Delete a event selected from its ID")
@click.argument("id")
def event_delete(id):
    try:
        with Session() as session:
            token = valid_token()
            permission = "delete-event"

            event_to_delete = Event.get_by_id(session, id)
            if not event_to_delete:
                return EventView.event_not_found_error()

            has_object_permission(permission, token, event_to_delete)

            event_to_delete.delete(session)
            EventView.event_deleted()
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
                    Event.contract.has(Contract.client.has(sales_contact_id=token["user_id"]))
                )
            elif token["role"] == "support":
                filters.append(
                    Event.support_contact_id == token["user_id"]
                )
        if no_support:
            filters.append(Event.support_contact_id == None)

        events = session.scalars(select(Event).where(*filters)).all()

        if not events:
            print("No event fit these requirements")
        else:
            for event in events:
                print(event)
