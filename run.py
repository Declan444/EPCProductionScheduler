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
SHEET = GSPREAD_CLIENT.open('EPC_Production_Schedule')


def get_sales_figures():
    """function to get sales data from the sales/day sheet """

    print('Please enter sales per day.')
    print('Sales data should be entered as 5 numbers, separated by commas.\n')

    sales_data = input('Enter your data here:')
    print(f'The data provide is {sales_data}')

get_sales_figures()