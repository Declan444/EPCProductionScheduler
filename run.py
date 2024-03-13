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
    while True:
        print('Please enter sales per day.')
        print('Sales figures should be entered as 5 numbers, separated by commas.\n')
    
    
        sales_data = input('Enter your data here:')
        sales_numbers = sales_data.split(',')
        
        if validate_data(sales_numbers):
            print('Numbers Validated', sales_numbers)
            return sales_numbers
        else:
            print('Invalid data: Please try again.\n')

def get_output_figures():
    """function to get sales data from the sales/day sheet """
    while True:
        print('Please enter line output numbers per day.')
        print('Line Output figures should be entered as 5 numbers, separated by commas.\n')
    
    
        line_output_data = input('Enter your data here:')
        output_numbers = line_output_data.split(',')
        
        if validate_data(output_numbers):
            print('Numbers Validated', output_numbers)
            return output_numbers
        else:
            print('Invalid data: Please try again.\n')

def get_manufactured_figures():
    """function to get manufactured volume data from the sales/day sheet """
    while True:
        print('Please enter Manufactured Volume .')
        print('Manufactured Volume figures should be entered as 5 numbers, separated by commas. If nothing was manufactured, enter zero.\n')
    
    
        manufactured_volume_data = input('Enter your data here:')
        volume_numbers = manufactured_volume_data.split(',')
        
        if validate_data(volume_numbers):
            print('Numbers Validated', volume_numbers)
            return volume_numbers
        else:
            print('Invalid data: Please try again.\n')
                  

def validate_data(values):
    try:
        if len(values) != 5 or not all(value.isdigit() for value in values):
            raise ValueError(
                f'Please enter 5 whole numbers separated by commas, you entered {values}'
            )
        return True
    except ValueError as e:
        print(f'Invalid data: {e}, please try again.\n')
        return False



def update_sales_worksheet(data):
    print('Updating sales worksheet....\n')
    if len(data) ==5 and all(isinstance(num, int) for num in data):
        sales_worksheet = SHEET.worksheet('salesPerDay')
        sales_worksheet.append_row(data)
        print('Sales worksheet updated successfully\n')
    else:
        print('Invalid data format: Unable to update the sales worksheet.\n')


def update_line_worksheet(data):
    print('Updating sales worksheet....\n')
    if len(data) ==5 and all(isinstance(num, int) for num in data):
        line_output_worksheet = SHEET.worksheet('lineOutput')
        line_output_worksheet.append_row(data)
        print('Line Output worksheet updated successfully\n')
    else:
        print('Invalid data format: Unable to update the line Output worksheet.\n')


def update_manufacturing_worksheet(data):
    print('Updating manufactured volume worksheet....\n')
    if len(data) ==5 and all(isinstance(num, int) for num in data):
        manufactured_worksheet = SHEET.worksheet('manufacturedVolume')
        manufactured_worksheet.append_row(data)
        print('Manufactured Volume worksheet updated successfully\n')
    else:
        print('Invalid data format: Unable to update the Manufactured Volume worksheet.\n')




data = get_sales_figures()
sales_data = [int(num) for num in data]
update_sales_worksheet(sales_data)

lineData = get_output_figures()
line_data = [int(num) for num in lineData]
update_line_worksheet(line_data)

manufacturedData = get_manufactured_figures()
manufactured_data = [int(num) for num in manufacturedData]
update_manufacturing_worksheet(manufactured_data)



