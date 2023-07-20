import re
from colorama import Fore


class Validator:
    def email(email):
        """
        Inside try raises ValueError if the email fails validation
        and returns False, prints information for the user about the error
        if no error - returns True
        validate email code and regex:
        https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
        """
        regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        try:
            if(not re.fullmatch(regex_email, email)):
                raise ValueError(f"The address '{email}' does not seem to be "
                                "correct")

        except ValueError as e:
            print(f"{Fore.RED}Invalid email: {e} please try again.\n")
            return False

        return True

    def room(room_number):
        """
        changes user input to integer and validates user input for choosing a room
        """

        try:
            # regex that accepts a number or a white space with number
            # https://stackoverflow.com/questions/50177113/regex-for-only-numbers-in-string

            regex_number = r'^([\s\d]+)$'

            if(not re.fullmatch(regex_number, room_number)):
                raise ValueError("You have entered other"
                                "characters than numbers\n")

            elif int(room_number) not in range(1, 10):

                raise ValueError(f"The room '{room_number}' does not seem to be "
                                "in the correct range 1 - 9\n")

        except ValueError as e:
            print(f"{Fore.RED}Invalid room number: {e} please try again.\n")
            return False

        return True

    def date_in_the_past(input_date):
        """
        tests if given date is in the past
        """
        today = datetime.today()
        # takes date input by the user in the format dd/mm/yyyy
        # and converts to a python date time object
        date_object = datetime.strptime(input_date, "%d/%m/%Y")

        if date_object < today:
            return True
        else:
            return False


    def date_not_in_worksheet(date_str):
        """
        check if date exists in the spreadsheet,
        currently period 01/09/2021 - 26/05/2024
        """
        existing_dates_rooms = rooms_worksheet.col_values(1)
        existing_dates_clients = clients_worksheet.col_values(1)
        if ((date_str not in existing_dates_rooms)
        or (date_str not in existing_dates_clients)):
            return True
        else:
            return False

    def validate_date(date):
        """
        Inside try raises ValueError if the date fails validation and returns False
        prints information for the user about the error
        if no error - returns True
        """
        # regex for date with leap year support
        # https://stackoverflow.com/questions/15491894/regex-to-validate-date-format-dd-mm-yyyy-with-leap-year-support
        #
        # how to split long regex
        # https://stackoverflow.com/questions/8006551/how-to-split-long-regular-expression-rules-to-multiple-lines-in-python/8006576#8006576

        regex_date = re.compile(
                    r'^(?:(?:31(\/)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|'
                    r'Dec)))\1|(?:(?:29|30)(\/)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|'
                    r'May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)\d'
                    r'{2})$|^(?:29(\/)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]'
                    r'|[2-9]\d)(?:0[48]|[2468][048]|[13579][26])'
                    r'|(?:(?:16|[2468][048]|[3579][26])00))))$|^'
                    r'(?:0?[1-9]|1\d|2[0-8])(\/)(?:(?:0?[1-9]|(?'
                    r':Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1'
                    r'[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]'
                    r'\d)\d{2})$', re.IGNORECASE)

        try:
            if(not re.fullmatch(regex_date, date)):
                raise ValueError(f"The date '{date}' does not seem to be "
                                "in the correct format\n")
            elif (Validator.date_in_the_past(date)):
                raise ValueError(f"The date '{date}' is not available\n"
                                f"we can only accept booking from\n"
                                f"tomorrow onwards,")
            elif Validator.date_not_in_worksheet(date):
                # assuming that administrator will extend both worksheets equaly.
                existing_dates_rooms = rooms_worksheet.col_values(1)
                last_row = len(existing_dates_rooms)
                max_date = read_cell_value(clients_worksheet, last_row, 1)
                raise ValueError(f"We can only accept booking between"
                                f" today and {max_date}\n")

        except ValueError as e:
            print(f"{Fore.RED}Invalid date: {e} please try again.\n")
            return False

        return True