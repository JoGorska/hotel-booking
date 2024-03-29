import gspread
from colorama import Fore
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

CLIENTS_WORKSHEET = SHEET.worksheet('clients')
ROOMS_WORKSHEET = SHEET.worksheet('rooms')



def update_one_cell(worksheet, row, column, value):
    """
    updates given worksheet with the given value in the exact
    one cell pointed by row and column
    row and column count starts from 1
    """
    # todo here need try and except to catch errors from gspread
    try:
        worksheet.update_cell(row, column, value)
    except Exception as e:
        print(f' some trouble here {e}')


def add_new_client(email):
    """
    Update clients worksheet, add email as a header
    of a next empty column and add new empty column
    """
    print("Adding your email to worksheet...\n")
    try:
        # ads new column so excel doesn't run out of cells

        CLIENTS_WORKSHEET.add_cols(1)
        # Coordinates to add email to customers worksheets:
        # row = 1 (first row in the worksheet)
        # column_number = need to check how many columns there is currently
        # and add email at the last column without values
        new_column_numer = len(CLIENTS_WORKSHEET.row_values(1)) + 1
        # uses coordinates calculated above to find the right cell to update
        print(f"{Fore.BLUE}Updating worksheet...\n")
        update_one_cell(CLIENTS_WORKSHEET, 1, new_column_numer, email)
        print("Worksheet updated successfuly.\n")
    except Exception as e:
        print(f' some trouble here {e}')

def find_a_row(value):
    """
    finds a cell that contains the given value and returns its row number
    """
    try:
        target_cell = CLIENTS_WORKSHEET.find(value)
        return target_cell.row
    except Exception as e:
        print(f' some trouble here {e}')


def find_a_column(worksheet, value):
    """
    finds a cell that contains the given value and return its column number
    """
    try:
        target_cell = worksheet.find(value)
        return target_cell.col
    except Exception as e:
        print(f' some trouble here {e}')


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


def read_cell_value(worksheet, row_no, col_no):
    """
    reads the value of the cell in the given worksheet,
    row and column coordinates
    """
    value = worksheet.cell(row_no, col_no).value
    return value
