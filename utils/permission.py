import click

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
            "assign-support-contact-to-event",
        ],
        "support": ["update-event"],
    }
    if not action in role_permission.get(token["role"], []):
        raise click.ClickException(
            "You do not have the permission to perform this action"
        )
