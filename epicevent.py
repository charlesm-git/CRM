import click

from commands.authenticationcommands import login, logout, current_user
from commands.usercommands import user_creation


@click.group()
def cli():
    pass


commands = [
    login,
    logout,
    current_user,
    user_creation,
]

for command in commands:
    cli.add_command(command)

if __name__ == "__main__":
    cli()
