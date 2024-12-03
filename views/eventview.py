from utils.validation import datetime_validation


class EventView:
    def __init__(self):
        pass

    @classmethod
    def event_creation_welcome_message(cls):
        print("Enter the new event information.")

    @classmethod
    def get_contract_id(cls):
        return input("Contract ID : ")

    @classmethod
    def event_creation(cls):
        while True:
            name = input("Name : ")
            if name != "":
                break
            
        while True:
            location = input("Location : ")
            if location != "":
                break
            print("Invalid input. Please make sure to enter a location")

        while True:
            attendees = input("Number of attendees : ")
            if attendees.isdigit():
                break
            print("Invalid input. Please make sure to enter a number")

        while True:
            start_date = input("Start date (format YYYY-MM-DD HH:MM): ")
            if datetime_validation(start_date):
                break
            print("Invalid input. Make sure to respect the format indicated.")
            
        while True:
            end_date = input("End date (format YYYY-MM-DD HH:MM): ")
            if datetime_validation(end_date):
                break
            print("Invalid input. Make sure to respect the format indicated.")
            
        note = input("Note (optional) : ")

        return {
            "name": name,
            "location": location,
            "attendees": attendees,
            "start_date": start_date,
            "end_date": end_date,
            "note": note,
        }

    @classmethod
    def event_update_support_contact_welcome_message(cls):
        print(
            "Enter the email of the user that will be the support contact for this event"
        )

    @classmethod
    def get_support_contact_email(cls):
        return input("Support contact email : ")

    @classmethod
    def event_update(cls):
        print(
            "Enter the information to update. Leave black to remain enchanged."
        )
        
        name = input("Name : ")
        location = input("Location : ")
        
        while True:
            attendees = input("Number of attendees : ")
            if attendees == "" or attendees.isdigit():
                break
            print("Invalid input. Please make sure to enter a number")

        while True:
            start_date = input("Start date (format YYYY-MM-DD HH:MM): ")
            if start_date == "" or datetime_validation(start_date):
                break
            print("Invalid input. Make sure to respect the format indicated.")
            
        while True:
            end_date = input("End date (format YYYY-MM-DD HH:MM): ")
            if end_date == "" or datetime_validation(end_date):
                break
            print("Invalid input. Make sure to respect the format indicated.")
            
        note = input("Note (optional) : ")

        return {
            "name": name,
            "location": location,
            "attendees": attendees,
            "start_date": start_date,
            "end_date": end_date,
            "note": note,
        }

    @classmethod
    def event_created(cls):
        print("Event created successfully")

    @classmethod
    def event_updated(cls):
        print("Event updated successfully")

    @classmethod
    def event_deleted(cls):
        print("Event deleted successfully")

    @classmethod
    def event_not_found_error(cls):
        print("Event not found")

    @classmethod
    def signed_status_error(cls):
        print(
            "The input for the signed status should be 0 or 1. The "
            "modification of the event status have been ignored. Other "
            "changes have been applied."
        )
