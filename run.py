import gspread
import re
import colorama
from google.oauth2.service_account import Credentials
from datetime import datetime
from colorama import Fore
from booking.images import Image
from booking.user_prompts import UserPrompt
from booking.rooms import room_full_name, room_short_name, change_room_name_to_number
colorama.init(autoreset=True)

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('hotel-booking')

clients_worksheet = SHEET.worksheet('clients')
rooms_worksheet = SHEET.worksheet('rooms')


def update_one_cell(worksheet, row, column, value):
    """
    updates given worksheet with the given value in the exact
    one cell pointed by row and column
    row and column count starts from 1
    """
    # todo here need try and except to catch errors from gspread
    worksheet.update_cell(row, column, value)



def add_new_client(email):
    """
    Update clients worksheet, add email as a header
    of a next empty column and add new empty column
    """
    print("Adding your email to worksheet...\n")

    clients_worksheet = SHEET.worksheet('clients')
    # ads new column so excel doesn't run out of cells
    # (oryginaly document contained a-z columns only)
    clients_worksheet.add_cols(1)
    # Coordinates to add email to customers worksheets:
    # row = 1 (first row in the worksheet)
    # column = need to check how many columns there is currently
    # and add email at the end

    new_column_numer = len(clients_worksheet.row_values(1)) + 1
    # uses coordinates calculated above to find the right cell to update
    print(f"{Fore.BLUE}Updating worksheet...\n")
    update_one_cell(clients_worksheet, 1, new_column_numer, email)
    print("Worksheet updated successfuly.\n")


room_number = 1


def find_a_row(value):
    """
    finds a cell that contains the given value and returns its row number
    """
    target_cell = clients_worksheet.find(value)

    return(target_cell.row)


def find_a_column(worksheet, value):
    """
    finds a cell that contains the given value and return its column number
    """
    target_cell = worksheet.find(value)

    return(target_cell.col)


def add_data_to_spreadsheet(worksheet, start, end, column_val, cell_value):
    """
    Adds name of the booked room to the appropriate cell
    in the client's spreadsheet
    Adds client's email to appropriate cell in rooms spreadsheet
    """
    # uses strings to locate the cell and gets the row numbers
    # for start and end date
    print(f"{Fore.BLUE}Updating worksheet {worksheet}...")
    row_start = find_a_row(start)
    row_end = find_a_row(end) + 1

    for row in range(row_start, row_end):

        column_number = find_a_column(worksheet, column_val)
        update_one_cell(worksheet, row, column_number, cell_value)


def is_too_short(start, end):
    """
    checks if the booked stay is too short
    """
    row_start = find_a_row(start)
    row_end = find_a_row(end)
    lenght = row_end - row_start
    if lenght < 7:
        return True
    else:
        return False


def is_too_long(start, end):
    """
    check if the booked stay is too long
    """
    row_start = find_a_row(start)
    row_end = find_a_row(end)
    lenght = row_end - row_start
    if lenght > 30:
        return True
    else:
        return False


def end_date_before_start(start, end):
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


def validate_lenght_of_stay(start, end):
    """
    Inside try raises ValueError if the length of stay fails validation
    and returns False prints information for the user about the error
    if no error - returns True
    """
    try:
        if is_too_short(start, end):
            raise ValueError("We can only accpet booking for "
                             "the minimum of 7 days\n")
        elif (is_too_long(start, end)):
            raise ValueError("We can only accept booking for "
                             "maximum of 30 days,\n please contact"
                             "the hotel if you require longer stay\n")
        elif (end_date_before_start(start, end)):
            raise ValueError("You have entered end date before start date\n")

    except ValueError as e:
        print(f"{Fore.RED}Invalid booking: {e} please try again.\n")
        return False

    return True


def read_cell_value(worksheet, row_no, col_no):
    """
    reads the value of the cell in the given worksheet,
    row and column coordinates
    """
    value = worksheet.cell(row_no, col_no).value
    return value


def is_any_empty_cell(worksheet, start_str, end_str, column):
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


def is_any_full_cell(worksheet, start_str, end_str, column):

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


def validate_room_availibility(start, end, room_int, email):
    """
    uses a function to validate the rooms' availability
    and returns an error if the room has already been booked on those dates
    """
    try:
        column_room = room_int + 1
        column_email = find_a_column(clients_worksheet, email)
        if (is_any_full_cell(rooms_worksheet, start, end, column_room) or
           is_any_full_cell(clients_worksheet, start, end, column_email)):
            raise ValueError("Unfortunately those dates are not available\n")

    except ValueError as e:
        print(f"{Fore.RED}Invalid booking: {e} please try again.\n")
        return False

    return True


def get_all_booking_info(email):
    """
    function to obtain both dates start and end date from the user
    returns a list containing two elements, start and end dates
    in a form of string - date as in excel
    """
    while True:
        print("We will now ask you to input your booking start date "
              "and end date, please follow the given date format\n")
        list_start_end_room = []
        # initializes functions to get user input for start and end date
        start = UserPrompt.start_date_input()
        list_start_end_room.append(start)
        end = UserPrompt.end_date_input()
        list_start_end_room.append(end)

        # initializes function to get user input for room number
        room = UserPrompt.get_room_int()
        list_start_end_room.append(room)
        if (validate_lenght_of_stay(start, end)
                and validate_room_availibility(start, end, room, email)):
            print(f"{Fore.GREEN}Booking validated.\n")
            break

    return list_start_end_room


def register_new_booking(email):
    """
    initializes two functions one after another, that are asking
    for the room, start date, and end date,
    than initializes adding the booked dates into the spreadsheets
    """
    print("To add new booking we will need the "
          "name of the room as well as start and end date\n")

    # initializes function to get all booking informations:
    # start and end dates and room number

    list_dates_room = get_all_booking_info(email)
    start_date_str = list_dates_room[0]
    end_date_str = list_dates_room[1]

    room_number = list_dates_room[2]
    # displays room name in two different formats
    booked_room_full_name = room_full_name(room_number)
    room_short = room_short_name(room_number)

    print(f"You entered booking for {booked_room_full_name} from "
          f"{start_date_str} to {end_date_str}\n")
    # ads the above data to spreadsheet
    print(f"{Fore.BLUE}Recording your booking in the spreadsheet...")
    add_data_to_spreadsheet(clients_worksheet, start_date_str,
                            end_date_str, email, room_short)
    add_data_to_spreadsheet(rooms_worksheet, start_date_str,
                            end_date_str, room_short, email)
    print("Worksheet updated.\n\n")


def get_cancelation_data(email):
    """
    gets a list containing cancelation data:
    start and end as strings and room as integer
    calls function to validate cancelation dates
    loops request for cancelation dates
    if validation of cancelation dates returned an error
    """
    while True:
        print("Please enter the start date and end date"
              " for the booking that you need to cancel")
        cancelation_data_list = []
        # gets the strings containing start and end dates
        # from the user
        start_str = UserPrompt.start_date_input()
        end_str = UserPrompt.end_date_input()

        # gets the room name and room number
        room_int = UserPrompt.get_room_int()
        room_short = room_short_name(room_int)

        # appends the strings to make the list with data
        # needed for deleting entries from spreadsheet
        cancelation_data_list.append(start_str)
        cancelation_data_list.append(end_str)
        cancelation_data_list.append(room_short)

        if validate_cancelation_dates(start_str, end_str, room_int, email):
            print(f"{Fore.GREEN}Valid cancellation dates")
            break

    return cancelation_data_list


def validate_cancelation_dates(start_str, end_str, room_int, email):
    """
    in try checks, if cell is empty - this way it
    checks if the period that client has put to be canceled,
    is a valid booking. Checks value of each cell within the
    date range in the column under email the client has given
    Raises ValueError if the cell was empty, there is nothing
    to cancel
    """

    try:

        column_email = find_a_column(clients_worksheet, email)

        column_room = room_int + 1

        if (is_any_empty_cell(clients_worksheet, start_str, end_str,
                              column_email) or
            is_any_empty_cell(rooms_worksheet, start_str, end_str,
                              column_room)):
            raise ValueError("There is no booking matching your criteria\n")

    except ValueError as e:
        print(f"{Fore.RED}Invalid cancelation dates: {e} please try again.\n")
        return False

    return True


def delete_booking_from_spreadsheet(email):
    """
    deletes booking from a spreadsheet
    """
    print("To cancel your booking please provide us with"
          " start and end date of the booking you want to cancel")
    # start date and end date strings come from
    # function get_cancelation_data

    cancelation_data_list = get_cancelation_data(email)
    start_date_str = cancelation_data_list[0]
    end_date_str = cancelation_data_list[1]

    # the cell value will be replaced with empty string
    cell_value = ""

    room_short_name = cancelation_data_list[2]

    # informs the client what is about to happen
    print(f"You are about to cancel booking for the period"
          f" between {start_date_str} and {end_date_str}")
    print(f"{Fore.BLUE} Deleting your booking from the spreadsheet...")

    # updates clients worksheet
    add_data_to_spreadsheet(clients_worksheet, start_date_str,
                            end_date_str, email, cell_value)
    # updates rooms worksheet

    add_data_to_spreadsheet(rooms_worksheet, start_date_str,
                            end_date_str, room_short_name, cell_value)


# Here start functions that deal with printing / displaying booking
# or showing room availibility


def make_list_of_dates(worksheet, row_start, row_end):
    """
    returns list of dates
    """
    # makes a list of values containing each date in excel format
    # (string dd/mm/yyyy)
    list_of_excel_dates = []
    # for loop gets each cell value and appends the list
    for row in range(row_start, (row_end + 1)):
        # gets the value of the cell in the column for the chosen room
        # and each row in within the booked period
        # column is "1" as the date strings are in the first column
        column = 1
        val = read_cell_value(worksheet, row, column)
        list_of_excel_dates.append(val)

    return list_of_excel_dates


def make_list_from_column(worksheet, row_start, row_end, column_value):
    """
    collects value from each cell in the given worksheet, column, and
    from row_start to row_end
    appends the value to the list_of_column_values
    """
    # makes a list of values containing each date in excel format
    # (string dd/mm/yyyy)
    list_of_column_values = []

    # for loop gets each cell value and appends the list

    for row in range(row_start, (row_end + 1)):
        # gets the value of the cell in the column for the chosen room
        # and each row in within the booked period of time
        # column is 1 as the date strings are in the first column

        column = find_a_column(worksheet, column_value)
        val = read_cell_value(worksheet, row, column)

        # this codes the value keeps it private
        # this allows printing column containing various users
        # emails without revealing the identity of who booked it.

        if (val == "") or (val is None):
            val = "None"
        elif "@" in val:
            val = "Reserved"

        list_of_column_values.append(val)

    return list_of_column_values


def make_dictionary_from_lists(list1, list2):
    """
    creates a dictionary from two lists
    code copied from code institute challenge for love sandwiches,
    the result that I wrote, based on love sandwiches presentation
    """

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


def validate_print_request(start, end):
    """
    Inside try raises ValueError if the user entered end date before
    the start date for the print request.
    """
    try:
        print("Validating print request...\n")
        if (end_date_before_start(start, end)):
            raise ValueError("You have entered end date before start date\n")

    except ValueError as e:
        print(f"{Fore.RED}Invalid print request: {e}\n please try again.\n")
        return False

    return True


def print_user_booking(email):
    """
    gets the dates from functions and initializes the functions to make
    lists and dictionary with data needed for the print
    lastly, it initializes the function to print the dictionary
    """
    while True:
        # obtains start and end date of the print from the user
        print("We will now ask you for a start and end date of\n"
              "the period that you want to print\n")
        start = UserPrompt.start_date_input()
        end = UserPrompt.end_date_input()

        # finds in which row those dates are
        row_start = find_a_row(start)
        row_end = find_a_row(end)

        # calls functions that create lists of data from the
        # appropriate columns and from start to end date
        print("Checking the spreadsheet...")
        list_column_dates = make_list_of_dates(clients_worksheet,
                                               row_start, row_end)
        list_column_email = make_list_from_column(clients_worksheet,
                                                  row_start, row_end, email)
        # makes dictionary out of two above lists
        dictionary = make_dictionary_from_lists(list_column_dates,
                                                list_column_email)

        if validate_print_request(start, end):
            print(f"{Fore.GREEN}Print request validated.\n")
            break

    print_dictionary(dictionary)


def show_room_availability():
    """
    gets the dates and room from functions and initializes the functions
    to make lists and a dictionary with data needed for the print
    lastly, it initializes the function to print the dictionary
    """
    while True:
        # obtains start and end date of the print from the user
        print("We will now ask you for a start and end date\n"
              "of the period that you want to check and than\n"
              "to give us the room number you would like\n")
        start = UserPrompt.start_date_input()
        end = UserPrompt.end_date_input()
        room_int = UserPrompt.get_room_int()
        room_name = room_short_name(room_int)

        # finds in which row those dates are
        row_start = find_a_row(start)
        row_end = find_a_row(end)

        # calls functions that create lists of data from the
        # appropriate columns and from start to end date
        print("Checking the spreadsheet...")
        list_column_dates = make_list_of_dates(rooms_worksheet,
                                               row_start, row_end)
        list_column_room = make_list_from_column(rooms_worksheet,
                                                 row_start, row_end,
                                                 room_name)
        # makes dictionary out of two above lists
        dictionary = make_dictionary_from_lists(list_column_dates,
                                                list_column_room)

        if validate_print_request(start, end):
            print(f"{Fore.GREEN}Print request validated.\n")
            break

    print_dictionary(dictionary)

# Here starts functions that handle user options


def get_returning_client_option():
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

        if validate_client_option(chosen_option):

            print(f"{Fore.GREEN}Your option is valid\n")
            break
    return chosen_option


def validate_client_option(option):
    """
    function to validate the option that returning customer
    has chosen
    """
    try:

        if option == "":
            # returns error when input is empty
            raise ValueError("You didn't choose any option.\n")

        elif (option != "add" and option != "print" and option != "change"
              and option != "cancel" and option != "quit"
              and option != "show"):
            # returns error if the given word does not match
            # any of the given options
            raise ValueError(f"The the word '{option}' does not\n seem to be "
                             f"matching any of the given options\n")

    except ValueError as e:
        print(f"{Fore.RED}Invalid option: {e} please try again.\n")
        return False

    return True


def get_new_client_option():

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

        if validate_new_client_option(chosen_option):

            print(f"{Fore.GREEN}Your option is valid\n")
            break
    return chosen_option


def validate_new_client_option(option):
    """
    function to validate the option that returning customer
    has chosen
    """
    try:

        if option == "":
            # returns error when input is empty
            raise ValueError("You didn't choose any option.\n")

        elif (option != "add" and option != "show"
                and option != "quit"):
            # returns error if the given word does not match
            # any of the given options
            raise ValueError(f"The the word '{option}' does not\n seem to be "
                             f"matching any of the given options\n")

    except ValueError as e:
        print(f"{Fore.RED}Invalid option: {e} please try again.\n")
        return False

    return True


def activate_chosen_option(option, email):
    """
    initializes the function depending on the function that the client has chosen
    """
    if option == "add":
        # uses provided email to register new booking,
        # initializes function to register new booking
        register_new_booking(email)

        # once the new booking is completed the client
        # gets the returning customer options

        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, email)

    elif option == "show":
        show_room_availability()
        chosen_option = get_new_client_option()
        activate_chosen_option(chosen_option, email)
        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, email)

    elif option == "print":

        print_user_booking(email)
        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, email)

    elif option == "change":
        print("To change your booking we will first ask you to delete "
              "the booking on the dates that need to be canceled and then"
              "to add the booking")
        delete_booking_from_spreadsheet(email)
        register_new_booking(email)
        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, email)

    elif option == "cancel":
        # initializes function to cancel booking
        delete_booking_from_spreadsheet(email)

        # once booking is cancelled the client
        # gets the returning customer options

        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, email)

    elif option == "quit":
        # prints a cat climbing into a box and
        # a goodbye message
        # ends the program
        print_cat()


def is_returning_client(email):
    """
    checks the clients worksheet if the email is already listed,
    prints welcome message for returning client or adds new client
    """
    # list of emails already added is in first row of clients worksheet
    clients_list = clients_worksheet.row_values(1)

    if email in clients_list:
        # welcomes returning customers
        print("Welcome back")
        return True

    else:
        # adds new customers to spreadsheet
        add_new_client(email)
        return False


def main():
    """
    Run all program functions
    """
    Image.print_image(Image.CASTLE)
    customer_email = UserPrompt.get_email()

    if is_returning_client(customer_email):
        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, customer_email)
    else:
        chosen_option = get_new_client_option()
        activate_chosen_option(chosen_option, customer_email)
        # once registration is complete -
        # client can choose from the given options what to do next
        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, customer_email)


main()
