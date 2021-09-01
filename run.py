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

rooms = SHEET.worksheet('rooms')


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


def add_new_client(email):
    """
    Update clients worksheet, add email as a header of a next empty column and add new empty column
    """
    print("Adding your email to worksheet...\n")
    
    clients_worksheet = SHEET.worksheet('clients')
    # ads new column so excel doesn't run out of cells (oryginaly document contained a-z columns only)

    clients_worksheet.add_cols(1)
    # Coordinates to add email to customers worksheets:
    # row = 1 (first row in the worksheet)
    # column = need to check how many columns there is currently and add email at the end

    new_column_numer = len(clients_worksheet.row_values(1)) + 1
    # uses coordinates 
    clients_worksheet.update_cell(1, new_column_numer, email)




customer_email = get_email_from_user()
add_new_client(customer_email)
