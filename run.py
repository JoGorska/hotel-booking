import gspread
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

def get_email_from_user():
    """
    Get email from the user
    """
    print("Please enter your email address")
    print("Example: email@domain.uk\n")
    customer_email = input("Enter your email here: ")
    print(f"Email that you have provided is {customer_email}")

get_email_from_user()