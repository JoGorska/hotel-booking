
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