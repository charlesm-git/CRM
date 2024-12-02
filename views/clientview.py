from utils.validation import email_validation, phone_number_validation


class ClientView:
    def __init__(self):
        pass

    @classmethod
    def client_creation(cls):
        print("Enter the new client information.")
        name = input("Name : ")
        surname = input("Surname : ")

        while True:
            email = input("Email : ")
            if email_validation(email):
                break
            print("Invalid format, try again.")

        while True:
            phone_number = input("Phone number : ")
            if phone_number_validation(phone_number) and phone_number.split():
                break
            print("Invalid format, try again.")

        company = input("Company (optional) : ")

        return {
            "name": name,
            "surname": surname,
            "email": email,
            "phone_number": phone_number,
            "company": company,
        }

    @classmethod
    def client_update(cls):
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

        while True:
            phone_number = input("Phone number : ")
            if phone_number == "" or (
                phone_number_validation(phone_number) and phone_number.split()
            ):
                break
            print("Invalid format, try again.")

        company = input("Company : ")

        return {
            "name": name,
            "surname": surname,
            "email": email,
            "phone_number": phone_number,
            "company": company,
        }

    @classmethod
    def client_created(cls):
        print("Client created successfully")

    @classmethod
    def client_updated(cls):
        print("Client updated successfully")

    @classmethod
    def client_deleted(cls):
        print("Client deleted successfully")

    @classmethod
    def client_not_found_error(cls):
        print("Client not found")
