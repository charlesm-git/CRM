from getpass import getpass

class AuthenticationView:
    def __init__(self):
        pass

    @staticmethod
    def get_credentials():
        email = input("Enter email : ")
        password = getpass("Enter password : ")
        return [email, password]

    @staticmethod
    def get_email_error():
        print("This email do not have an account.")
        
    @staticmethod
    def get_mismatch_error():
        print("Email and password do not match.")
    
    @staticmethod
    def login_successfull():
        print("Login successfull")