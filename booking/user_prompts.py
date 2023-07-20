
from colorama import Fore
from .validators import Validator


class UserPrompt:
    def get_email():
        """
        Get email from the user, validate user email input
        and return customer email input
        """
        while True:
            print("Please enter your email address")
            print("Example: email@domain.uk\n")

            customer_email_input = input("Enter your email here: \n")
            customer_email_input = customer_email_input.lower()
            print(f"You entered {customer_email_input}\n")

            if Validator.email(customer_email_input):
                print(f"{Fore.GREEN}Your email is valid\n")
                break

        return customer_email_input

    def get_room_int():
    """
    gives options to choose which room to book
    """
    while True:
        print("Please choose one of rooms:")
        print("1. Kew Gardens Suite")
        print("2. Oxford Suite")
        print("3. London Suite")
        print("4. Verulamium Suite")
        print("5. Cambridge Botanic Gardens")
        print("6. Stonehenge Suite")
        print("7. Lucretia's Suite")
        print("8. Glasgow Suite")
        print("9. Ware Suite\n")
        global room_number
        room_number = input("Write a number 1 - 9: \n")

        if Validator.room(room_number):

            print(f"{Fore.GREEN}Your room is valid\n")
            break
    return int(room_number)