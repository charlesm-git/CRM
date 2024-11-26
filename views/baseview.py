class BaseView:
    def __init__(self):
        pass

    @staticmethod
    def user_creation_view():
        name = input("name : ")
        surname = input("surname : ")
        email = input("email : ")
        password = input("password : ")
        role = input("role (1: sales / 2: management / 3: support) : ")
        return {
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,
            "role": role,
        }
