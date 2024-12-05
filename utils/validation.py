import jwt
import click
import re
from datetime import datetime
from argon2 import PasswordHasher

SECRET_KEY = "This_is_the_secret_key"


def load_token():
    """Load the JWT from the .twt file"""
    try:
        with open("token.txt", "r") as token_file:
            return token_file.read()
    except FileNotFoundError:
        raise click.ClickException(
            "You are not logged in. Please, log in first."
        )


def valid_token():
    """Check if the JWT is still valid"""
    token = load_token()
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise click.ClickException(
            "Your session has expired. Please log in again"
        )
    except jwt.InvalidTokenError:
        raise click.ClickException("Invalid token. Please log in again")


def hash_password(password):
    """Hash a password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)


def email_validation(email):
    """Validate the email format"""
    email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)


def role_validation(role_id):
    """validate the input of the user to attribute a role"""
    return int(role_id) in [1, 2, 3]


def phone_number_validation(phone_number):
    """Validate the phone number format"""
    number_regex = r"[0-9+ ]+$"
    return re.match(number_regex, phone_number)


def signed_status_validation(signed_status):
    """Validate the user input for the contract signed status boolean"""
    return signed_status in ["0", "1", ""]


def datetime_validation(date):
    """Validate the datetime format"""
    try:
        datetime.strptime(date, "%Y-%m-%d %H:%M")
        return True
    except ValueError:
        return False
