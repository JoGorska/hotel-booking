import gspread
import re
from google.oauth2.service_account import Credentials

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

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def validate_email(email):
    """
    Inside try raises ValueError if the email fails validation and returns False
    prints information for the user about the error
    if no error - returns True
    """
    try:
        if(not re.fullmatch(regex, email)):
            raise ValueError(f"The address '{email}' does not seem to be correct")

    except ValueError as e:
        print(f"Invalid email: {e}, please try again.\n")
        return False

    return True




def update_one_cell(worksheet, row, column, value):
    """
    updates given worksheet with the given value in the exact one cell pointed by row and column
    row and column count starts from 1
    """
    print(f"Updating worksheet...\n")
    worksheet.update_cell(row, column, value)
    print("Worksheet updated successfuly.\n")

def add_new_client(email):
    """
    Update clients worksheet, add email as a header of a next empty column and add new empty column
    ??? uncomment new column when spreasheet full
    """
    print("Adding your email to worksheet...\n")
    
    clients_worksheet = SHEET.worksheet('clients')
    # ads new column so excel doesn't run out of cells (oryginaly document contained a-z columns only)

    # clients_worksheet.add_cols(1)
    # Coordinates to add email to customers worksheets:
    # row = 1 (first row in the worksheet)
    # column = need to check how many columns there is currently and add email at the end

    new_column_numer = len(clients_worksheet.row_values(1)) + 1
    # uses coordinates calculated above to find the right cell to update
    update_one_cell(clients_worksheet, 1, new_column_numer, email)

def start_date_input():
    """
    Prompts client to input start date for the booking
    """
    print("To add new booking we will need start and end date")
    print("For dates please use format dd/mm/yyyy\n")
    start_date = input("Write start date here: ")

def end_date_input():
    """
    Prompts client to input end date for the booking
    """
    end_date = input("Write end date here: ")

def new_booking():
    start_date_input()
    end_date_input()

def returning_client_options():
    """
    gives returning client various options to choose from
    runs appropriate function after the option is choosen
    """
    print("Please choose option to add a new booking (add), check your booking (print), change your booking (change), cancel your booking (cancel)\n")
    client_options = input("Write 'add', 'print', 'change' or 'cancel' here: ")
    validate_client_options()

def validate_client_options():
    print("I am checking if input for client options is valid")

def check_if_returning_client(email):
    """
    checks the clients worksheet if the email is already listed, 
    prints welcome messag for returning client or adds new client
    """
    # list of emails already added is in first row of clients worksheet
    clients_list = clients_worksheet.row_values(1)

    if email in clients_list:
        # welcomes returning customers
        print("Welcome back to Cath's Cats' Castle!\n")

        returning_client_options()
        
    else:
        # adds new customers to spreadsheet
        add_new_client(email)
        new_booking()


customer_email = get_email_from_user()
check_if_returning_client(customer_email)
