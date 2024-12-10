from getpass import getpass
from rich import print


def get_credentials():
    email = input("Enter email : ")
    password = getpass("Enter password : ")
    return [email, password]


def get_email_error():
    return "This email do not have an account."


def get_mismatch_error():
    return "Email and password do not match."


def login_successfull():
    return print("[bold green]Login successfull[/bold green]")


def logout_successfull():
    return print("[bold cyan]Logout successfull[/bold cyan]")
