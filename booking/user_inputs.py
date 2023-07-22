
from colorama import Fore
from .validators import (
    DateValidator,
    RoomValidator,
    EmailValidator, NewClientOptionsValidator, ReturningClientOptionsValidator
)


class UserInput:
    @classmethod
    def email(cls):
        """
        Get email from the user, validate user email input
        and return customer email input
        """
        while True:
            print(
                "Please enter your email address\n"
                "Example: email@domain.uk\n"
            )

            customer_email_input = input("Enter your email here: \n")
            customer_email_input = customer_email_input.lower() if customer_email_input else ''
            print(f'You entered "{customer_email_input}"\n')

            if EmailValidator(validated_object=customer_email_input, object_type='email').result:
                print(f"{Fore.GREEN}Your email is valid\n")
                break
        return customer_email_input

    @classmethod
    def new_client_option(cls):
        """
        gives new client various options to choose from
        function returns a chosen option
        """

        while True:
            print(
                "Please choose one of the following options:"
                "add a new booking (add)"
                "show room availability (show),"
                "quit the program (quit)\n")
            chosen_option = input(
                "Write 'add', 'show' or 'quit' here: \n"
            )

            # if OptionsValidator.new_client_options(chosen_option):
            if NewClientOptionsValidator(chosen_option, 'option').result:

                print(f"{Fore.GREEN}Your option is valid\n")
                break
        return chosen_option

    @classmethod
    def returning_client_option(cls):
        """
        gives returning client various options to choose from
        returns the option
        """

        while True:
            print(
                "Please choose one of the following options:"
                "to add a new booking (add)"
                "show room availability (show),"
                "check your booking (print),"
                "change your booking (change),"
                "cancel your booking (cancel)"
                "quit the program (quit)\n"
            )
            chosen_option = input("Write 'add', 'show', 'print', "
                                  "'change', 'cancel' or 'quit' here: \n")

            if ReturningClientOptionsValidator(chosen_option, 'option').result:
                print(f"{Fore.GREEN}Your option is valid\n")
                break
            return chosen_option

    @classmethod
    def room_integer(cls):
        """
        gives options to choose which room to book
        """
        while True:
            print(
                "Please choose one of rooms:"
                "1. Kew Gardens Suite"
                "2. Oxford Suite"
                "3. London Suite"
                "4. Verulamium Suite"
                "5. Cambridge Botanic Gardens"
                "6. Stonehenge Suite"
                "7. Lucretia's Suite"
                "8. Glasgow Suite"
                "9. Ware Suite\n")
            room_number = 1
            room_number = input("Write a number 1 - 9: \n")

            if RoomValidator.room(room_number):

                print(f"{Fore.GREEN}Your room is valid\n")
                break
        return int(room_number)

    @property
    def start_date(self):
        """
        Prompts client to input start date for the booking
        """
        while True:
            print("Please use format dd/mm/yyyy for dates\n")
            start_date = input("Write start date here: \n")

            if DateValidator.validate_date(DateValidator, start_date):
                print(f"{Fore.GREEN}Your date is in valid format.\n")

                break

        return start_date

    @property
    def end_date(self):
        """
        Prompts client to input end date for the booking
        """
        while True:
            print("Please use format dd/mm/yyyy for dates\n")
            end_date = input("Write end date here: \n")

            if DateValidator.validate_date(DateValidator, end_date):
                print(f"{Fore.GREEN}Your date is in valid format.\n")
                break
        return end_date