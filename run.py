import colorama
from booking.images import Image
from booking.user_inputs import UserInput
from booking.validators import (
    ReturningClientValidator
)
from booking.worksheet_utils import add_new_client

from booking.client_options import ClientOptions

colorama.init(autoreset=True)


def main():
    """
    Run all program functions
    """
    print(Image.CASTLE)
    customer_email = UserInput.email()

    if ReturningClientValidator(customer_email, 'email').check_object_is_a_member():
        print("Welcome back")
        chosen_option = UserInput.returning_client_option()
        ClientOptions.activate_chosen_option(chosen_option, customer_email)
    else:
        # adds new customers to spreadsheet
        add_new_client(customer_email)
        chosen_option = UserInput.new_client_option()
        ClientOptions.activate_chosen_option(chosen_option, customer_email)
        # once registration is complete -
        # client can choose from the given options what to do next
        chosen_option = UserInput.returning_client_option
        ClientOptions.activate_chosen_option(chosen_option, customer_email)


main()
