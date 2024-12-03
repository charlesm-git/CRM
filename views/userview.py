from utils.validation import email_validation, role_validation


class UserView:
    def __init__(self):
        pass

    @classmethod
    def user_creation(cls):
        print("Enter the new user information.")
        
        while True:
            name = input("Name : ")
            if name != "":
                break
        
        while True:
            surname = input("Surname : ")
            if surname != "":
                break

        while True:
            email = input("Email : ")
            if email_validation(email):
                break
            print("Invalid format, try again.")

        while True:
            password = input("Password : ")
            if password != "":
                break

        while True:
            role_id = input("Role (1: sales / 2: management / 3: support) : ")
            if role_validation(role_id):
                break
            print("Invalid input, try again.")

        return {
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,
            "role_id": role_id,
        }

    @classmethod
    def user_update(cls):
        print(
            "Enter the information to update. Leave black to remain enchanged."
        )
        name = input("Name : ")
        surname = input("Surname : ")

        while True:
            email = input("Email : ")
            if email == "" or email_validation(email):
                break
            print("Invalid format, try again.")

        password = input("Password : ")

        while True:
            role_id = input("Role (1: sales / 2: management / 3: support) : ")
            if role_id == "" or role_validation(role_id):
                break
            print("Invalid input, try again.")

        return {
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,
            "role_id": role_id,
        }

    @classmethod
    def user_created(cls):
        print("User created successfully")

    @classmethod
    def user_updated(cls):
        print("User updated successfully")

    @classmethod
    def user_deleted(cls):
        print("User deleted successfully")

    @classmethod
    def user_not_found_error(cls):
        print("User not found")
