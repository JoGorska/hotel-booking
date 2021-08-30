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

data = rooms.get_all_values()

customer_email = ""
def get_email_from_user():
    """
    Get email from the user
    """
    global customer_email
    print("Please enter your email address")
    print("Example: email@domain.uk\n")
    customer_email = input("Enter your email here: ")
    print(f"Email that you have provided is {customer_email}\n")
    return customer_email

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def validate_email(email):
    """
    Validates email input from the user
    
    """
    if(re.fullmatch(regex, email)):
        print("Valid Email")
 
    else:
        print("Please enter valid email address")
        print("Example: email@domain.uk\n")

# validate email code:
# https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
get_email_from_user()
validate_email(customer_email)