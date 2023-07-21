
from colorama import Fore
from .validators import Validator, OptionsValidator


class UserInput:
    @property
    def email(self):
        """
        Get email from the user, validate user email input
        and return customer email input
        """
        while True:
            print("Please enter your email address")
            print("Example: email@domain.uk\n")

            customer_email_input = input("Enter your email here: \n")
            customer_email_input = customer_email_input.lower() if customer_email_input else ''
            print(f'You entered "{customer_email_input}"\n')

            if Validator.email(customer_email_input):
                print(f"{Fore.GREEN}Your email is valid\n")
                break

        return customer_email_input

    @property
    def returning_client_option(self):
        """
        gives returning client various options to choose from
        returns the option
        """

        while True:
            print("Please choose one of the following options:")
            print("to add a new booking (add)")
            print("show room availability (show),")
            print("check your booking (print),")
            print("change your booking (change),")
            print("cancel your booking (cancel)")
            print("quit the program (quit)\n")
            chosen_option = input("Write 'add', 'show', 'print', "
                                  "'change', 'cancel' or 'quit' here: \n")

            if OptionsValidator.returning_client_options(chosen_option):
                print(f"{Fore.GREEN}Your option is valid\n")
                break
        return chosen_option

    @property
    def new_client_option(self):

        """
        gives new client various options to choose from
        function returns a chosen option
        """

        while True:
            print("Please choose one of the following options:")
            print("add a new booking (add)")
            print("show room availability (show),")
            print("quit the program (quit)\n")
            chosen_option = input("Write 'add', 'show', "
                                  "or 'quit' here: \n")

            if OptionsValidator.new_client_options(chosen_option):

                print(f"{Fore.GREEN}Your option is valid\n")
                break
        return chosen_option

    @property
    def room_integer(self):
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
            room_number = 1
            room_number = input("Write a number 1 - 9: \n")

            if Validator.room(room_number):

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

            if Validator.validate_date(start_date):
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

            if Validator.validate_date(end_date):
                print(f"{Fore.GREEN}Your date is in valid format.\n")
                break
        return end_date
