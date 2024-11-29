from getpass import getpass

class AuthenticationView:
    def __init__(self):
        pass

    @classmethod
    def get_credentials(cls):
        email = input("Enter email : ")
        password = getpass("Enter password : ")
        return [email, password]

    @classmethod
    def get_email_error(cls):
        return "This email do not have an account."
        
    @classmethod
    def get_mismatch_error(cls):
        return "Email and password do not match."
    
    @classmethod
    def login_successfull(cls):
        return print("Login successfull")