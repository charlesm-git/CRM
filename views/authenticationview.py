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
    def get_login_error():
        print("Invalid email or password.")
    
    @staticmethod
    def login_successfull():
        print("Login successfull")