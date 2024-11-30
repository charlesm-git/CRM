import click

from commands.authentication import login, logout, current_user
from commands.user import user_create, user_update, user_delete, user_list


@click.group()
def cli():
    pass


commands = [
    login,
    logout,
    current_user,
    user_create,
    user_update,
    user_delete,
    user_list,
]

for command in commands:
    cli.add_command(command)

if __name__ == "__main__":
    cli()
