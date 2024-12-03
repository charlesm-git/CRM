class ContractView:
    def __init__(self):
        pass

    @classmethod
    def contract_creation_welcome_message(cls):
        print("Enter the new contract information.")

    @classmethod
    def get_client_id(cls):
        return input("Client ID : ")

    @classmethod
    def contract_creation(cls):
        while True:
            total_contract_amount = input("Total amount of the contract : ")
            if total_contract_amount.isdigit():
                break
            print("Invalid input. Please make sure to enter a number")

        while True:
            remaining_amount_to_pay = input(
                "Remaining amount to pay (Leave blank if nothing has been payed yet) : "
            )
            if remaining_amount_to_pay == "" or remaining_amount_to_pay.isdigit():
                break
            print("Invalid input. Please make sure to enter a number")

        return {
            "total_contract_amount": total_contract_amount,
            "remaining_amount_to_pay": remaining_amount_to_pay,
        }

    @classmethod
    def contract_update(cls):
        print(
            "Enter the information to update. Leave black to remain enchanged."
        )
        while True:
            total_contract_amount = input("Total amount of the contract : ")
            if total_contract_amount == "" or total_contract_amount.isdigit():
                break
            print("Invalid input. Please make sure to enter a number")

        while True:
            remaining_amount_to_pay = input("Remaining amount to pay : ")
            if (
                remaining_amount_to_pay == ""
                or remaining_amount_to_pay.isdigit()
            ):
                break
            print("Invalid input. Please make sure to enter a number")

        contract_signed_status = input(
            "Contract signed status (0: unsigned / 1: signed) : "
        )

        return {
            "total_contract_amount": total_contract_amount,
            "remaining_amount_to_pay": remaining_amount_to_pay,
            "contract_signed_status": contract_signed_status,
        }

    @classmethod
    def contract_created(cls):
        print("Contract created successfully")

    @classmethod
    def contract_updated(cls):
        print("Contract updated successfully")

    @classmethod
    def contract_deleted(cls):
        print("Contract deleted successfully")

    @classmethod
    def contract_not_found_error(cls):
        print("Contract not found")

    @classmethod
    def signed_status_error(cls):
        print(
            "The input for the signed status should be 0 or 1. The "
            "modification of the contract status have been ignored. Other "
            "changes have been applied."
        )
