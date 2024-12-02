import jwt
import click
import re
from argon2 import PasswordHasher

SECRET_KEY = "This_is_the_secret_key"

def load_token():
    """Load the JWT from the .twt file"""
    try:
        with open("token.txt", "r") as token_file:
            return token_file.read()
    except FileNotFoundError:
        raise click.ClickException("You are not logged in. Please, log in first.")


def valid_token():
    """Check if the JWT is still valid"""
    token = load_token()

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise click.ClickException("Your session has expired. Please log in again")
    except jwt.InvalidTokenError:
        raise click.ClickException("Invalid token. Please log in again")

def hash_password(password):
    ph = PasswordHasher()
    return ph.hash(password)

def email_validation(email):
    email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_regex, email)

def role_validation(role_id):
    return int(role_id) in [1, 2, 3]

def phone_number_validation(phone_number):
    number_regex = r"[0-9+ ]+$"
    return re.match(number_regex, phone_number)
