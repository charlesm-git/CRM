from models.client import Client
from models.contract import Contract
from models.event import Event


def has_permission(action, token):
    """
    Check a permission.
    Raise an PermissionError if the access is not granted.
    """
    role_permission = {
        "sales": [
            "create-client",
            "update-client",
            "delete-client",
            "update-contract",
            "create-event",
            "update-event",
            "delete-event",
        ],
        "management": [
            "create-user",
            "update-user",
            "delete-user",
            "create-contract",
            "update-contract",
            "delete-contract",
            "update-support-event",
        ],
        "support": [
            "update-event",
            "delete-event",
        ],
    }
    if not action in role_permission.get(token["role"], []):
        raise PermissionError(
            "You do not have the permission to perform this action"
        )


def has_object_permission(action, token, object):
    """
    Checks an object level permission.
    Raise a PermissionError is the permission is not granted.
    """
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

    if type(object) is Event:
        # Support contact of the event and sales contact of the client can
        # modify the event
        if (
            object.support_contact_id == token["user_id"]
            or object.contract.client.sales_contact_id == token["user_id"]
        ):
            return

    raise PermissionError(
        "You do not have the object permission to perform this action"
    )
