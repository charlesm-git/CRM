class UserView:
    def __init__(self):
        pass

    @classmethod
    def user_creation_view(cls):
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

    @classmethod
    def user_created(cls):
        return print("User creation successfull")