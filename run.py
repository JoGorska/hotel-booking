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

clients = SHEET.worksheet('clients')




def get_email_from_user():
    """
    Get email from the user
    """
    while True:
        print("Please enter your email address")
        print("Example: email@domain.uk\n")

        customer_email_input = input("Enter your email here: ")

        print(f"You entered {customer_email_input}\n")
        
        if validate_email(customer_email_input):
            print("Your email is valid")
            break


# validate email code and regex:
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def validate_email(email):
    """
    Validates email input from the user
    
    """
    try:
        if(not re.fullmatch(regex, email)):
            raise ValueError(f"The address '{email}' does not seem to be correct")

    except ValueError as e:
        print(f"Invalid email: {e}, please try again.\n")
        return False

    return True



customer_email = get_email_from_user()
