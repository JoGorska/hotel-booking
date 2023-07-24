
from colorama import Fore
from booking.images import Image
from booking.user_inputs import UserInput
from booking.validators import (
    LengthOfStayValidator, AvailibilityValidator, validate_print_request
)
from booking.rooms import (
    room_full_name, room_short_name
)
from booking.worksheet_utils import (
    clients_worksheet, rooms_worksheet,
    find_a_row, find_a_column, add_data_to_spreadsheet, read_cell_value
)


class ClientOptions:

    ADD = 'add'
    SHOW = 'show'
    PRINT = 'print'
    CHANGE = 'change'
    CANCEL = 'cancel'
    QUIT = 'quit'

    RETURNING_CLIENT_OPTIONS = [
        ADD, PRINT, CHANGE, CANCEL, QUIT, SHOW
    ]

    NEW_CLIENT_OPTIONS = [
        ADD, SHOW, QUIT
    ]

    @classmethod
    def activate_chosen_option(cls, option, email):
        """
        initializes the function depending on the right option class
        that the client has chosen. Each class has run_option method
        """
        map_options = {
            ClientOptions.ADD: OptionAdd.run_option(email),
            ClientOptions.SHOW: OptionShow.run_option(email),
            ClientOptions.PRINT: OptionPrint.run_option(email),
            ClientOptions.CHANGE: OptionChange.run_option(email),
            ClientOptions.CANCEL: OptionCancel.run_option(email),
            ClientOptions.QUIT: OptionQuit.run_option(),

        }
        map_options.get(option)


class OptionAdd:
    name = ClientOptions.ADD

    @classmethod
    def run_option(cls, email):
        '''
        takes email to register new booking,
        initializes function to register new booking
        '''
        OptionAdd.register_new_booking(email)

        # once the new booking is completed the client
        # gets the returning customer options

        chosen_option = UserInput.returning_client_option()
        ClientOptions.activate_chosen_option(chosen_option, email)

    @classmethod
    def register_new_booking(cls, email):
        """
        initializes two functions one after another, that are asking
        for the room, start date, and end date,
        than initializes adding the booked dates into the spreadsheets
        """
        print(
            "To add new booking we will need the "
            "name of the room as well as start and end date\n")

        # initializes function to get all booking informations:
        # start and end dates and room number

        list_dates_room = OptionAdd.get_all_booking_info(email)
        start_date_str = list_dates_room[0]
        end_date_str = list_dates_room[1]

        room_number = list_dates_room[2]
        # displays room name in two different formats
        booked_room_full_name = room_full_name(room_number)
        room_short = room_short_name(room_number)

        print(
            f"You entered booking for {booked_room_full_name} from "
            f"{start_date_str} to {end_date_str}\n")
        # ads the above data to spreadsheet
        print(f"{Fore.BLUE}Recording your booking in the spreadsheet...")
        add_data_to_spreadsheet(
            clients_worksheet, start_date_str,
            end_date_str, email, room_short)
        add_data_to_spreadsheet(
            rooms_worksheet, start_date_str,
            end_date_str, room_short, email)
        print("Worksheet updated.\n\n")

    @classmethod
    def get_all_booking_info(cls, email):
        """
        function to obtain both dates start and end date from the user
        returns a list containing two elements, start and end dates
        in a form of string - date as in excel
        """
        while True:
            print(
                "We will now ask you to input your booking start date "
                "and end date, please follow the given date format\n")
            list_start_end_room = []
            # initializes functions to get user input for start and end date
            start = UserInput.start_date()
            list_start_end_room.append(start)
            end = UserInput.end_date()
            list_start_end_room.append(end)

            # initializes function to get user input for room number
            room = UserInput.room_integer()
            list_start_end_room.append(room)
            if (LengthOfStayValidator.validate_lenght_of_stay(
                LengthOfStayValidator, start, end) and (
                    AvailibilityValidator.validate_room_availibility(
                        AvailibilityValidator, start, end, room, email))):
                print(f"{Fore.GREEN}Booking validated.\n")
                break

        return list_start_end_room


class OptionShow:
    name = ClientOptions.SHOW

    @classmethod
    def run_option(cls, email):
        OptionShow.show_room_availability()
        chosen_option = UserInput.new_client_option()
        ClientOptions.activate_chosen_option(chosen_option, email)
        chosen_option = UserInput.returning_client_option()
        ClientOptions.activate_chosen_option(chosen_option, email)

    @classmethod
    def show_room_availability(cls):
        """
        gets the dates and room from functions and initializes the functions
        to make lists and a dictionary with data needed for the print
        lastly, it initializes the function to print the dictionary
        """
        while True:
            # obtains start and end date of the print from the user
            print(
                "We will now ask you for a start and end date\n"
                "of the period that you want to check and than\n"
                "to give us the room number you would like\n")
            start = UserInput.start_date()
            end = UserInput.end_date()
            room_int = UserInput.room_integer()
            room_name = room_short_name(room_int)

            # finds in which row those dates are
            row_start = find_a_row(start)
            row_end = find_a_row(end)

            # calls functions that create lists of data from the
            # appropriate columns and from start to end date
            print("Checking the spreadsheet...")
            list_column_dates = make_list_of_dates(
                rooms_worksheet, row_start, row_end)
            list_column_room = make_list_from_column(
                rooms_worksheet, row_start, row_end, room_name)
            # makes dictionary out of two above lists
            dictionary = make_dictionary_from_lists(list_column_dates,
                                                    list_column_room)

            if validate_print_request(start, end):
                print(f"{Fore.GREEN}Print request validated.\n")
                break

        print_dictionary(dictionary)


class OptionPrint:
    name = ClientOptions.PRINT

    @classmethod
    def run_option(cls, email):
        OptionPrint.print_user_booking(email)
        chosen_option = UserInput.returning_client_option()
        ClientOptions.activate_chosen_option(chosen_option, email)

    @classmethod
    def print_user_booking(cls, email):
        """
        gets the dates from functions and initializes the functions to make
        lists and dictionary with data needed for the print
        lastly, it initializes the function to print the dictionary
        """
        while True:
            # obtains start and end date of the print from the user
            print(
                "We will now ask you for a start and end date of\n"
                "the period that you want to print\n")
            start = UserInput.start_date()
            end = UserInput.end_date()

            # finds in which row those dates are
            row_start = find_a_row(start)
            row_end = find_a_row(end)

            # calls functions that create lists of data from the
            # appropriate columns and from start to end date
            print("Checking the spreadsheet...")
            list_column_dates = make_list_of_dates(
                clients_worksheet, row_start, row_end)
            list_column_email = make_list_from_column(
                clients_worksheet, row_start, row_end, email)
            # makes dictionary out of two above lists
            dictionary = make_dictionary_from_lists(
                list_column_dates, list_column_email)

            if validate_print_request(start, end):
                print(f"{Fore.GREEN}Print request validated.\n")
                break

        print_dictionary(dictionary)


class OptionChange:
    name = ClientOptions.CHANGE

    @classmethod
    def run_option(cls, email):
        print(
            "To change your booking we will first ask you to delete "
            "the booking on the dates that need to be canceled and then"
            "to add the booking")
        OptionCancel.delete_booking_from_spreadsheet(email)
        OptionAdd.register_new_booking(email)
        chosen_option = UserInput.returning_client_option()
        ClientOptions.activate_chosen_option(chosen_option, email)


class OptionCancel:
    name = ClientOptions.CANCEL

    @classmethod
    def run_option(cls, email):

        OptionCancel.delete_booking_from_spreadsheet(email)

        # once booking is cancelled the client
        # gets the returning customer options

        chosen_option = UserInput.returning_client_option()
        ClientOptions.activate_chosen_option(chosen_option, email)

    @classmethod
    def delete_booking_from_spreadsheet(cls, email):
        """
        deletes booking from a spreadsheet
        """
        print(
            "To cancel your booking please provide us with"
            " start and end date of the booking you want to cancel")
        # start date and end date strings come from
        # function get_cancelation_data

        cancelation_data_list = UserInput.cancelation_data(email)
        start_date_str = cancelation_data_list[0]
        end_date_str = cancelation_data_list[1]

        # the cell value will be replaced with empty string
        cell_value = ""

        room_short_name_str = cancelation_data_list[2]

        # informs the client what is about to happen
        print(
            "You are about to cancel booking for the period"
            f" between {start_date_str} and {end_date_str}")
        print(f"{Fore.BLUE} Deleting your booking from the spreadsheet...")

        # updates clients worksheet
        add_data_to_spreadsheet(clients_worksheet, start_date_str,
                                end_date_str, email, cell_value)
        # updates rooms worksheet

        add_data_to_spreadsheet(rooms_worksheet, start_date_str,
                                end_date_str, room_short_name_str, cell_value)


class OptionQuit:
    name = ClientOptions.QUIT

    @classmethod
    def run_option(cls):
        # prints a cat climbing into a box and
        # a goodbye message and ends the program
        print(Image.CAT)


def make_dictionary_from_lists(list1, list2):

    zip_iterator = zip(list1, list2)
    a_dictionary = dict(zip_iterator)
    return a_dictionary


def print_dictionary(dictionary):
    """
    support function to print the dictionary so that each
    key and value pairs are on a separate line,
    this should make the print more user friendly
    """
    print("Checking spreadsheet...")
    # prints one date below another, which will let the user
    # scroll through the results.
    for i in dictionary:
        print(i + ": " + dictionary[i])


def encode_values(worksheet, column_value, row):
    # gets the value of the cell in the column for the chosen room
    # and each row in within the booked period of time
    # column is 1 as the date strings are in the first column

    column = find_a_column(worksheet, column_value)
    val = read_cell_value(worksheet, row, column)

    # this codes the value keeps it private
    # this allows printing column containing various users
    # emails without revealing the identity of who booked it.
    encoded_value = 'Reserved' if val else 'None'
    return encoded_value


def make_list_from_column(worksheet, row_start, row_end, column_value):
    """
    collects value from each cell in the given worksheet, column, and
    from row_start to row_end
    appends the value to the list_of_column_values
    """
    # makes a list of values containing each date in excel format
    # (string dd/mm/yyyy)

    list_of_column_values = [
        encode_values(worksheet, column_value, row) for row in range(row_start, (row_end + 1))
    ]
    return list_of_column_values


def make_list_of_dates(worksheet, row_start, row_end):
    """
    returns list of dates
    """
    # makes a list of values containing each date in excel format
    # (string dd/mm/yyyy)

    # gets the value of the cell in the column for the chosen room
    # and each row in within the booked period
    # column is "1" as the date strings are in the first column
    column = 1
    list_of_excel_dates = [
        read_cell_value(worksheet, row, column) for row in range(row_start, (row_end + 1))
    ]
    return list_of_excel_dates
