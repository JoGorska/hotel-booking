import re
from datetime import datetime
from colorama import Fore
from booking.worksheet_utils import (
    CLIENTS_WORKSHEET, ROOMS_WORKSHEET,
    find_a_row, find_a_column, read_cell_value
)


MINIMUM_STAY = 2
MAXIMUM_STAY = 7


class BaseValidator:
    fail_on_empty = None
    regex = None
    raise_error_when_membership_test_fails = False

    def __init__(
            self,
            validated_object,
            object_type,
            second_validated_object=None,):

        self.validated_object = validated_object
        self.second_validated_object = second_validated_object
        self.object_type = object_type

        self.list_where_object_must_be_member = self.get_list_where_object_must_be_member()
        self.list_where_object_must_not_be_member = []
        self.result = self.run_validators()

    def get_list_where_object_must_be_member(self):
        return []

    def validate_if_empty(self):
        '''
        raises error if validated object is falsly (empty or None)
        validator only raises error if fail_on_empty is set to true
        '''
        if not self.fail_on_empty:
            return True
        if not self.validated_object:
            raise ValueError('No user input,')
        return True

    def validate_regex(self):
        '''
        checks if validated_object matches given regex
        if no regex is provided, validator returns True
        '''
        if not self.regex:
            return True

        if not re.fullmatch(self.regex, str(self.validated_object)):
            raise ValueError(
                f"The {self.object_type} does not seem to be correct,"
            )
        return True

    def check_object_is_a_member(self):
        '''
        this function is just testing for membership,
        it does not raise errors, just returns true or false.
        It is used to test membership and also to validate object is a member
        it is the validate_object_is_a_member that raises error
        '''
        if not self.list_where_object_must_be_member:
            return True
        elif self.validated_object in self.list_where_object_must_be_member:
            return True
        return False

    def validate_object_is_a_member(self):
        '''
        this validator only runs when
        raise_error_when_membership_test_fails is set to True
        '''
        if not self.raise_error_when_membership_test_fails:
            return True
        if not self.check_object_is_a_member():
            raise ValueError(
                f"The {self.object_type} was not found"
            )

    def validate_object_is_not_a_member(self):
        '''
        validation passes if object is not a member of the list
        '''
        if not self.list_where_object_must_not_be_member:
            return True
        if self.validated_object in self.list_where_object_must_not_be_member:
            raise ValueError(
                f"{self.validated_object} is already taken"
            )

    def run_validators(self):
        '''
        runs all validators, raises error if any of them returns error
        '''
        try:
            self.validate_if_empty()
            self.validate_regex()
            self.validate_object_is_a_member()
            self.validate_object_is_not_a_member()
        except ValueError as e:
            print(f"{Fore.RED}Invalid {self.object_type}: {e} please try again.\n")
            return False

        return True


class EmailValidator(BaseValidator):
    '''
    provides arguments for base validator to run validators on empty and regex
    regex for email from:
    https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    '''
    fail_on_empty = True
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class ReturningClientValidator(BaseValidator):
    '''checks if email is already in excel'''

    def get_list_where_object_must_be_member(self):
        '''list of clients' emails already added is in first row of clients worksheet'''
        return CLIENTS_WORKSHEET.row_values(1)


class NewClientOptionsValidator(BaseValidator):
    '''
    checks if user chose an option and if option is one of the given option choices
    list_where_object_must_be_member is a list of valid options
    '''
    fail_on_empty = True
    raise_error_when_membership_test_fails = True

    def get_list_where_object_must_be_member(self):
        # need to import here due to circular import error
        from .client_options import ClientOptions # noqa
        return ClientOptions.NEW_CLIENT_OPTIONS

    def validate_object_is_a_member(self):
        '''
        customises error message when object fails membership test
        '''
        if not self.check_object_is_a_member():
            print(self.validated_object)
            raise ValueError(
                f"The the word '{self.validated_object}' does not\nseem to be "
                f"matching any of the given options,\n")


class ReturningClientOptionsValidator(BaseValidator):
    '''
    checks if user chose an option and if option is one of the given option choices
    list_where_object_must_be_member is a list of valid options
    '''
    fail_on_empty = True
    raise_error_when_membership_test_fails = True

    def get_list_where_object_must_be_member(self):
        # need to import here due to circular import error
        from .client_options import ClientOptions # noqa
        return ClientOptions.RETURNING_CLIENT_OPTIONS

    def validate_object_is_a_member(self):
        '''
        customises error message when object fails membership test
        '''
        if not self.check_object_is_a_member():
            raise ValueError(
                f"The the word '{self.validated_object}' does not\n seem to be "
                f"matching any of the given options,\n")


class DateValidator(BaseValidator):
    """
    Inside try raises ValueError if the date fails validation and returns False
    prints information for the user about the error
    if no error - returns True

    regex for date with leap year support
    https://stackoverflow.com/questions/15491894/regex-to-validate-date-format-dd-mm-yyyy-with-leap-year-support

    how to split long regex
    https://stackoverflow.com/questions/8006551/how-to-split-long-regular-expression-rules-to-multiple-lines-in-python/8006576#8006576
    """

    fail_on_empty = True
    raise_error_when_membership_test_fails = True
    regex = re.compile(
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

    def validate_date_not_in_the_past(self):
        """
        tests if given date is in the past
        """
        today = datetime.today()
        # takes date input by the user in the format dd/mm/yyyy
        # and converts to a python date time object
        date_object = datetime.strptime(self.validated_object, "%d/%m/%Y")

        if date_object < today:
            raise ValueError(
                f"The date '{self.validated_object}' is not available\n"
                f"we can only accept booking from\n"
                f"tomorrow onwards,")
        return True

    def list_dates_available_worksheet_rooms(self):
        """
        check if date exists in the spreadsheet,
        currently period 01/09/2021 - 26/05/2024,
        this can be mainatined by the administrator if needed
        """
        return ROOMS_WORKSHEET.col_values(1)

    def list_dates_available_worksheet_clients(self):
        """
        check if date exists in the spreadsheet,
        currently period 01/09/2021 - 26/05/2024,
        this can be mainatined by the administrator if needed
        """
        return CLIENTS_WORKSHEET.col_values(1)

    def validate_object_is_a_member(self):
        '''
        this validator only runs when
        raise_error_when_membership_test_fails is set to True
        '''
        # assuming that administrator will extend both worksheets equaly.
        if not self.raise_error_when_membership_test_fails:
            return True
        if not self.check_object_is_a_member():
            existing_dates_rooms = ROOMS_WORKSHEET.col_values(1)
            last_row = len(existing_dates_rooms)
            max_date = read_cell_value(CLIENTS_WORKSHEET, last_row, 1)
            raise ValueError(
                f"We can only accept booking between"
                f" tomorrow and {max_date}\n")
        return True
    # add list for membership test - test if in client worksheet
    # and second list test if in rooms worksheet

    # than collect it all in new run validators function

    def run_validators(self):
        '''
        runs all validators, raises error if any of them returns error
        '''
        try:
            self.validate_if_empty()
            self.validate_regex()
            self.validate_date_not_in_the_past()
            # self.list - one, than list two
            self.list_where_object_must_be_member = self.list_dates_available_worksheet_rooms()
            self.validate_object_is_not_a_member()
            self.list_where_object_must_be_member = self.list_dates_available_worksheet_clients()
            self.validate_object_is_a_member()
        except ValueError as e:
            print(f"{Fore.RED}Invalid {self.object_type}: {e} please try again.\n")
            return False

        return True


class EndDateValidator(DateValidator):
    def validate_is_not_too_short(self):
        """
        checks if the booked stay is too short
        """
        end = self.validated_object
        start = self.second_validated_object
        row_start = find_a_row(start)
        row_end = find_a_row(end)
        lenght = row_end - row_start
        if lenght < MINIMUM_STAY:
            raise ValueError(
                "We can only accpet booking for "
                f"the minimum of {MINIMUM_STAY} days\n")
        return True

    def validate_is_not_too_long(self):
        """
        check if the booked stay is too long
        """
        end = self.validated_object
        start = self.second_validated_object
        row_start = find_a_row(start)
        row_end = find_a_row(end)
        lenght = row_end - row_start
        if lenght > MAXIMUM_STAY:
            raise ValueError(
                "We can only accept booking for "
                f"maximum of {MAXIMUM_STAY} days,\n please contact"
                "the hotel if you require longer stay\n")

        return True

    def validate_end_date_not_before_start(self):
        """
        check if end date was enetered before start date
        """
        end = self.validated_object
        start = self.second_validated_object
        row_start = find_a_row(start)
        row_end = find_a_row(end)
        lenght = row_end - row_start
        if lenght < 0:
            raise ValueError("You have entered end date before start date\n")
        return True

    def run_validators(self):
        try:
            super().run_validators()
            self.validate_is_not_too_short()
            self.validate_is_not_too_long()
            self.validate_end_date_not_before_start()
        except ValueError as e:
            print(f"{Fore.RED}Invalid {self.object_type}: {e} please try again.\n")
            return False

        return True


class RoomNumberValidator(BaseValidator):
    '''
    validates input on empty and regex
    regex that accepts a number or a white space with number
    https://stackoverflow.com/questions/50177113/regex-for-only-numbers-in-string
    '''
    fail_on_empty = True
    regex = r'^([\s\d]+)$'

    def get_list_where_object_must_be_member(self):
        print(range(1, 10))
        return range(1, 10)

    def validate_object_is_a_member(self):
        '''
        assuming regex number validator was passed, I can now safely change object to integer
        '''
        self.validated_object = int(self.validated_object)
        if self.validated_object not in self.list_where_object_must_be_member:
            raise ValueError(f"The room '{self.validated_object}' does not seem to be "
                             "in the correct range 1 - 9\n")


class RoomValidator:
    @classmethod
    def room(cls, room_number):
        """
        changes user input to integer and validates user input for choosing a room
        """

        try:
            # regex that accepts a number or a white space with number
            # https://stackoverflow.com/questions/50177113/regex-for-only-numbers-in-string

            regex_number = r'^([\s\d]+)$'

            if not re.fullmatch(regex_number, room_number):
                raise ValueError("You have entered other"
                                 "characters than numbers\n")

            elif int(room_number) not in range(1, 10):
                raise ValueError(f"The room '{room_number}' does not seem to be "
                                 "in the correct range 1 - 9\n")

        except ValueError as e:
            print(f"{Fore.RED}Invalid room number: {e} please try again.\n")
            return False

        return True

# todo remove this - all this is in end date validator
class LengthOfStayValidator:
    def is_too_short(self, start, end):
        """
        checks if the booked stay is too short
        """
        row_start = find_a_row(start)
        row_end = find_a_row(end)
        lenght = row_end - row_start
        if lenght < MINIMUM_STAY:
            return True
        else:
            return False

    def is_too_long(self, start, end):
        """
        check if the booked stay is too long
        """
        row_start = find_a_row(start)
        row_end = find_a_row(end)
        lenght = row_end - row_start
        if lenght > MAXIMUM_STAY:
            return True
        else:
            return False

    def end_date_before_start(self, start, end):
        """
        check if end date was enetered before start date
        """
        row_start = find_a_row(start)
        row_end = find_a_row(end)
        lenght = row_end - row_start
        if lenght < 0:
            return True
        else:
            return False

    def validate_lenght_of_stay(self, start, end):
        """
        Inside try raises ValueError if the length of stay fails validation
        and returns False prints information for the user about the error
        if no error - returns True
        """
        try:
            if self.is_too_short(start, end):
                raise ValueError(
                    "We can only accpet booking for "
                    "the minimum of 7 days\n")
            elif self.is_too_long(start, end):
                raise ValueError(
                    "We can only accept booking for "
                    "maximum of 30 days,\n please contact"
                    "the hotel if you require longer stay\n")
            elif self.end_date_before_start(start, end):
                raise ValueError("You have entered end date before start date\n")

        except ValueError as e:
            print(f"{Fore.RED}Invalid booking: {e} please try again.\n")
            return False

        return True


class AvailibilityValidator:
    def is_any_empty_cell(self, worksheet, start_str, end_str, column):
        """
        checks if the cell is empty,
        cell coordinates calculated from
        start and end date strings
        """
        print("Checking if any of the cells are empty...")
        # gets integer - exact row number for the date
        # that customer has provided
        row_start = find_a_row(start_str)
        row_end = find_a_row(end_str)

        result = []
        for row in range(row_start, (row_end + 1)):
            # gets the value of the cell in the column for the choosen room
            # and each row in within the booked period of time
            val = read_cell_value(worksheet, row, column)

            # if cell is empty - returns true, as room is available to book
            if val is None:
                result.append("true")

            else:

                result.append("false")

        if "true" in result:
            print("At least one of the cells was empty.")
            return True
        else:
            print("None of the cells were empty.")
            return False

    def is_any_full_cell(self, worksheet, start_str, end_str, column):

        """
        checks if any of the cells are full
        """
        print("Checking if any of the dates are taken...")
        # gets integer - exact row number for the date
        # that customer has provided
        row_start = find_a_row(start_str)
        row_end = find_a_row(end_str)

        result = []
        for row in range(row_start, (row_end + 1)):
            # gets the value of the cell in the column for the choosen room
            # and each row in within the booked period of time
            val = read_cell_value(worksheet, row, column)

            # if cell is empty - returns true, as room is available to book
            if val is None:
                result.append("false")
            else:
                result.append("true")

        if "true" in result:
            print("At least one of the dates is taken.")
            return True
        else:
            print("None of the dates are taken.")
            return False

    def validate_room_availibility(self, start, end, room_int, email):
        """
        uses a function to validate the rooms' availability
        and returns an error if the room has already been booked on those dates
        """
        try:
            column_room = room_int + 1
            column_email = find_a_column(CLIENTS_WORKSHEET, email)
            if (self.is_any_full_cell(ROOMS_WORKSHEET, start, end, column_room) or
                    self.is_any_full_cell(CLIENTS_WORKSHEET, start, end, column_email)):
                raise ValueError("Unfortunately those dates are not available\n")

        except ValueError as e:
            print(f"{Fore.RED}Invalid booking: {e} please try again.\n")
            return False

        return True

    def validate_cancelation_dates(self, start_str, end_str, room_int, email):
        """
        in try checks, if cell is empty - this way it
        checks if the period that client has put to be canceled,
        is a valid booking. Checks value of each cell within the
        date range in the column under email the client has given
        Raises ValueError if the cell was empty, there is nothing
        to cancel
        """

        try:

            column_email = find_a_column(CLIENTS_WORKSHEET, email)

            column_room = room_int + 1

            if (self.is_any_empty_cell(
                    CLIENTS_WORKSHEET, start_str, end_str, column_email
                    ) or
                self.is_any_empty_cell(
                    ROOMS_WORKSHEET, start_str, end_str, column_room)):
                raise ValueError("There is no booking matching your criteria\n")

        except ValueError as e:
            print(f"{Fore.RED}Invalid cancelation dates: {e} please try again.\n")
            return False

        return True


def validate_print_request(start, end):
    """
    Inside try raises ValueError if the user entered end date before
    the start date for the print request.
    """
    try:
        print("Validating print request...\n")
        if (LengthOfStayValidator.end_date_before_start(LengthOfStayValidator, start, end)):
            raise ValueError("You have entered end date before start date\n")

    except ValueError as e:
        print(f"{Fore.RED}Invalid print request: {e}\n please try again.\n")
        return False

    return True
