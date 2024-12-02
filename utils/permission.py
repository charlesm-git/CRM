import click

from models.client import Client
from models.contract import Contract
from views.clientview import ClientView
from views.contractview import ContractView


def has_permission(action, token):
    role_permission = {
        "sales": [
            "create-client",
            "update-client",
            "delete-client",
            "update-contract",
            "create-event",
            "update-event",
        ],
        "management": [
            "create-user",
            "update-user",
            "delete-user",
            "create-contract",
            "update-contract",
            "delete-contract",
            "update-event",
        ],
        "support": ["update-event"],
    }
    if not action in role_permission.get(token["role"], []):
        raise PermissionError(
            "You do not have the permission to perform this action"
        )


def has_object_permission(action, token, object):

    # Check the general permission
    has_permission(action, token)

    # Check the object permission
    if type(object) is Client:
        # Checks that the current user is the sales_contact of the client
        if object.sales_contact_id == token["user_id"]:
            return

    if type(object) is Contract:
        # Management has the right to update all contracts
        # Otherwise only the sales contact can update the contract
        if (
            token["role"] == "management"
            or object.client.sales_contact_id == token["user_id"]
        ):
            return

    raise PermissionError(
        "You do not have the object permission to perform this action"
    )
