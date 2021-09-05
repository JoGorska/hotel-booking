import gspread
import re
from google.oauth2.service_account import Credentials
from datetime import datetime


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


def get_email_from_user():
    """
    Get email from the user, validate user email input
    and return customer email input
    """
    while True:
        print("Please enter your email address")
        print("Example: email@domain.uk\n")

        customer_email_input = input("Enter your email here: ")

        print(f"You entered {customer_email_input}\n")

        if validate_email(customer_email_input):
            print("Your email is valid\n")
            break
    return customer_email_input

# validate email code and regex:
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/


def validate_email(email):
    """
    Inside try raises ValueError if the email fails validation
    and returns False, prints information for the user about the error
    if no error - returns True
    """
    regex_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    try:
        if(not re.fullmatch(regex_email, email)):
            raise ValueError(f"The address '{email}' does not seem to be "
                             "correct")

    except ValueError as e:
        print(f"Invalid email: {e}, please try again.\n")
        return False

    return True


def update_one_cell(worksheet, row, column, value):
    """
    updates given worksheet with the given value in the exact
    one cell pointed by row and column
    row and column count starts from 1
    """
    worksheet.update_cell(row, column, value)


def add_new_client(email):
    """
    Update clients worksheet, add email as a header
    of a next empty column and add new empty column
    ??? uncomment new column when spreasheet full
    """
    print("Adding your email to worksheet...\n")

    clients_worksheet = SHEET.worksheet('clients')
    # ads new column so excel doesn't run out of cells
    # (oryginaly document contained a-z columns only)
    # ??? unmute when spreadsheet full
    # clients_worksheet.add_cols(1)
    # Coordinates to add email to customers worksheets:
    # row = 1 (first row in the worksheet)
    # column = need to check how many columns there is currently
    # and add email at the end

    new_column_numer = len(clients_worksheet.row_values(1)) + 1
    # uses coordinates calculated above to find the right cell to update
    print("Updating worksheet...\n")
    update_one_cell(clients_worksheet, 1, new_column_numer, email)
    print("Worksheet updated successfuly.\n")


room_number = 1


def choose_room():
    """
    gives options to choose which room to book
    """

    while True:
        print("Please choose one of our luxury rooms:")
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
        room_number = input("Write a number 1 - 9: ")

        if validate_room(room_number):

            print("Your room is valid\n")
            break
    return int(room_number)


def validate_room(room_number):
    """
    changes user input to integer and validates user input for choosing a room
    """

    try:
        room_number = int(room_number)
        if room_number not in range(1, 10):
            raise ValueError(f"The room '{room_number}' does not seem to be "
                             "in the correct format")

    except ValueError as e:
        print(f"Invalid room number: {e}, please try again.\n")
        return False

    return True


def room_full_name(room_number):
    """
    takes customer's choise of a room number and returns room name
    """
    if room_number == 1:
        return "Kew Gardens Suite"
    elif room_number == 2:
        return "Oxford Suite"
    elif room_number == 3:
        return "London Suite"
    elif room_number == 4:
        return "Verulamium Suite"
    elif room_number == 5:
        return "Cambridge Botanic Gardens"
    elif room_number == 6:
        return "Stonehenge Suite"
    elif room_number == 7:
        return "Lucretia's Suite"
    elif room_number == 8:
        return "Glasgow Suite"
    elif room_number == 9:
        return "Ware Suite"


def room_short_name(room_number):
    """
    takes customer's choise of a room number and returns room name
    """
    if room_number == 1:
        return "Kew"
    elif room_number == 2:
        return "Oxford"
    elif room_number == 3:
        return "London"
    elif room_number == 4:
        return "Verulamium"
    elif room_number == 5:
        return "Cambridge"
    elif room_number == 6:
        return "Stonehenge"
    elif room_number == 7:
        return "Lucretia"
    elif room_number == 8:
        return "Glasgow"
    elif room_number == 9:
        return "Ware"


def start_date_input():
    """
    Prompts client to input start date for the booking
    """
    while True:
        print("Please use format dd/mm/yyyy for dates\n")
        start_date = input("Write start date here: ")

        if validate_date(start_date):
            print("Your date is valid\n")

            break

    return start_date


def end_date_input():
    """
    Prompts client to input end date for the booking
    """
    while True:
        print("Please use format dd/mm/yyyy for dates\n")
        end_date = input("Write end date here: ")

        if validate_date(end_date):
            print("Your date is in valid format\n")
            break
    return end_date


def convert_input_to_date(input_date):
    """
    takes date input by the user in the format dd/mm/yyyy and converts
    to a python date time object
    """
    date_object = datetime.strptime(input_date, "%d/%m/%Y")
    return date_object


def date_in_the_past(input_date):
    """
    tests if given date is in the past
    """
    today = datetime.today()
    date_object = convert_input_to_date(input_date)

    if date_object < today:
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

    regex_date = r'^(?:(?:31(\/)(?:0?[13578]|1[02]|(?:Jan|Mar|May|Jul|Aug|Oct|Dec)))\1|(?:(?:29|30)(\/)(?:0?[1,3-9]|1[0-2]|(?:Jan|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec))\2))(?:(?:1[6-9]|[2-9]\d)\d{2})$|^(?:29(\/)(?:0?2|(?:Feb))\3(?:(?:(?:1[6-9]|[2-9]\d)(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/)(?:(?:0?[1-9]|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep))|(?:1[0-2]|(?:Oct|Nov|Dec)))\4(?:(?:1[6-9]|[2-9]\d)\d{2})$'
    try:
        if(not re.fullmatch(regex_date, date)):
            raise ValueError(f"The date '{date}' does not seem to be "
                             "in the correct format")
        elif (date_in_the_past(date)):
            raise ValueError(f"The date '{date}' is in the past")

    except ValueError as e:
        print(f"Invalid date: {e}, please try again.\n")
        return False

    return True


def find_a_row(value):
    """
    finds a cell that contains the given value and returns it's row number
    """
    target_cell = clients_worksheet.find(value)

    return(target_cell.row)


def find_a_column(worksheet, value):
    """
    finds a cell that contains the given value and return it's column number
    """
    target_cell = worksheet.find(value)

    return(target_cell.col)


def add_booking_to_spreadsheet(worksheet, start, end, column_val, cell_value):
    """
    Adds name of the booked room to the appropriate cell
    in the client's spreadsheet
    Adds client's email to appropriate cell in rooms spreaedsheet
    """
    # uses strings to locate the cell and gets the row numbers
    # for start and end date
    row_start = find_a_row(start) - 1
    row_end = find_a_row(end)

    for row in range(row_start, row_end):

        column_number = find_a_column(worksheet, column_val)
        update_one_cell(worksheet, row, column_number, cell_value)
        print(f"updated {worksheet} cell {row} out of {row_end}"
              f"in the column {column_val} number {column_number}")


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


def is_too_long(start, end,):
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


def validate_lenght_of_stay(start, end):
    """
    Inside try raises ValueError if the lenght of stay fails validation
    and returns False prints information for the user about the error
    if no error - returns True
    """
    try:
        if is_too_short(start, end):
            raise ValueError("We can only accpet booking for "
                             "the minimum of 7 days")
        elif (is_too_long(start, end)):
            raise ValueError("We can only accept booking for "
                             "maximum of 30 days, please contact"
                             "the hotel if you require longer stay")

    except ValueError as e:
        print(f"Invalid booking: {e}, please try again.\n")
        return False

    return True


def read_cell_value(worksheet, row_no, col_no):
    """
    reads the value of the cell in the given worksheet,
    row and column coordinates
    """
    value = worksheet.cell(row_no, col_no).value
    return value


def is_avialable(start, end, room_int):
    """
    checks the rooms worksheet to see if the room is
    available in the dates given by the customer
    """
    # gets integer - exact row number for the date
    # that customer has provided
    row_start = find_a_row(start)
    row_end = find_a_row(end)
    column_room = room_int + 1

    for row in range(row_start, row_end):
        # gets the value of the cell in the column for the choosen room
        # and each row in within the booked period of time
        val = read_cell_value(rooms_worksheet, row, column_room)

        # if cell is empty - returns true, as room is available to book
        if val == "":

            return True
        else:

            return False


def validate_room_availibility(start, end, room_int):
    """
    uses a function to validate the rooms' availiblity
    and returns error if the room has already been booked in those dates
    """
    try:
        if (not is_avialable(start, end, room_int)):
            raise ValueError("Unfortunately this room is booked "
                             "in these dates")

    except ValueError as e:
        print(f"Invalid booking: {e}, please try again.\n")
        return False

    return True


def get_all_booking_info():
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
        start = start_date_input()
        list_start_end_room.append(start)
        end = end_date_input()
        list_start_end_room.append(end)

        # initializes function to get user input for room number
        room = choose_room()
        list_start_end_room.append(room)

        if (validate_lenght_of_stay(start, end)
                and validate_room_availibility(start, end, room)):
            print("Booking validated. Saving in the spreadsheet...\n")
            break

    return list_start_end_room


def register_new_booking(email):
    """
    initializes two functions one after enother, that are asking
    for room, start date and end date,
    than initializes adding the booked dates into the spreadsheets
    """
    print("To add new booking we will need the "
          "name of the room as well as start and end date\n")

    # initializes function to get all booking informations:
    # start and end dates and room number

    list_dates_room = get_all_booking_info()
    start_date_str = list_dates_room[0]
    end_date_str = list_dates_room[1]

    room_number = list_dates_room[2]
    # displays room name in two different formats
    booked_room_full_name = room_full_name(room_number)
    room_short = room_short_name(room_number)

    print(f"You entered booking for {booked_room_full_name} from "
          f"{start_date_str} to {end_date_str}\n")
    # ads the above data to spreadsheet
    print("Recording your booking in the worksheet...")
    add_booking_to_spreadsheet(clients_worksheet, start_date_str,
                               end_date_str, email, room_short)
    add_booking_to_spreadsheet(rooms_worksheet, start_date_str,
                               end_date_str, room_short, email)
    print("Worksheet updated.")


def get_returning_client_option():
    """
    gives returning client various options to choose from
    returns the option
    """

    while True:
        print("Please choose one of the following options:")
        print("to add a new booking (add)")
        print("check your booking (print),")
        print("change your booking (change),")
        print("cancel your booking (cancel)\n")
        chosen_option = input("Write 'add', 'print', "
                              "'change' or 'cancel' here: ")

        if validate_client_option(chosen_option):

            print("Your option is valid\n")
            break
    return chosen_option


def validate_client_option(option):
    """
    function to validate the option that returning customer
    has chosen
    """

    try:

        if (option != "add" and option != "print"
                and option != "change" and option != "cancel"):
            # returns error if the given word does not match
            # any of the given options
            raise ValueError(f"The the word '{option}' does not seem to be "
                             "matching any of the given options")

    except ValueError as e:
        print(f"Invalid option: {e}, please try again.\n")
        return False

    return True


def activate_chosen_option(option, email):
    """
    initializes the function depending on the function that client has chosen
    """
    if option == "add":
        # uses provided email to register new booking, initializes function to register
        register_new_booking(email)
    elif option == "print":
        print(f"The option '{option}'' is currently not working. We are working on it.")
    elif option == "change":
        print(f"The option '{option}'' is currently not working. We are working on it.")
    elif option == "cancel":
        print(f"The option '{option}'' is currently not working. We are working on it.")

def is_returning_client(email):
    """
    checks the clients worksheet if the email is already listed,
    prints welcome messag for returning client or adds new client
    """
    # list of emails already added is in first row of clients worksheet
    clients_list = clients_worksheet.row_values(1)

    if email in clients_list:
        # welcomes returning customers
        print("Welcome back to Cath's Cats' Castle!\n")
        return True

    else:
        # adds new customers to spreadsheet
        add_new_client(email)
        return False


def main():
    """
    Run all program functions
    """
    customer_email = get_email_from_user()

    if is_returning_client(customer_email):
        chosen_option = get_returning_client_option()
        activate_chosen_option(chosen_option, customer_email)
    else:
        register_new_booking(customer_email)


main()
