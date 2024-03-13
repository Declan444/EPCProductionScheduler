import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint
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
    """function to get sales data from the sales sheet """
    while True:
        print('Please enter line output numbers per day.')
        print('Line Output figures should be entered as 5 numbers, separated by commas.\n')
    
    
        line_output_data = input('Enter your data here:')
        output_numbers = line_output_data.split(',')
        # To check the validate function against the data
        if validate_data(output_numbers):
            print('Numbers Validated', output_numbers)
            return output_numbers
        else:
            print('Invalid data: Please try again.\n')

def get_manufactured_figures():
    """function to get manufactured volume data from the sales sheet """
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
    """
    Validation function to ensure that the data type entered is 5 in length and are integers
    """
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
    """
    Function to update the sales worksheet. Have just copied this for the line and production worksheet
    """
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


def available_stock():
    """
    Function to get the lineOutput data and add it to the last line of the available stock data and subtract the sales data to give an updated available stock data. This gives me available stock to work with and an accumulated number.
    """
    print('Calculating available stock...\n')

    line_output_worksheet = SHEET.worksheet('lineOutput')
    available_stock_worksheet = SHEET.worksheet('AvailableStockUnits')
    sales_worksheet = SHEET.worksheet('salesPerDay')

    # To get the last row from the "lineOutput" worksheet
    last_line_output_row = line_output_worksheet.get_all_values()[-1]

    # If there is data in the last row
    if last_line_output_row:
        # To convert the values to integers
        last_line_output_values = [int(num) for num in last_line_output_row]

        # To get the last row from the "AvailableStockUnits" worksheet
        last_available_stock_row = available_stock_worksheet.get_all_values()[-1]

        # When there is data in the last row of the sheet, then add the corresponding values
        if last_available_stock_row:
            last_available_stock_values = [int(num) for num in last_available_stock_row]
            new_row_values = [str(output + stock) for output, stock in zip(last_line_output_values, last_available_stock_values)]
        else:
            # When there is no data in the "AvailableStockUnits" worksheet, use the current line output values
            new_row_values = [str(num) for num in last_line_output_values]

        # To get the last row from the "salesPerDay" worksheet
        last_sales_row = sales_worksheet.get_all_values()[-1]

        # If there is data in the last sales row, subtract the sales values
        if last_sales_row:
            last_sales_values = [int(num) for num in last_sales_row]
            # Make sure that both data types are integers
            new_row_values = [str(int(stock) - sales) for stock, sales in zip(new_row_values, last_sales_values)]

       
        available_stock_worksheet.append_row(new_row_values)
        print('Available Stock updated successfully\n')
    else:
        print('Not enough data in the "lineOutput" sheet.')
   
    
    





def main():
    data = get_sales_figures()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)

    lineData = get_output_figures()
    line_data = [int(num) for num in lineData]
    update_line_worksheet(line_data)

    manufacturedData = get_manufactured_figures()
    manufactured_data = [int(num) for num in manufacturedData]
    update_manufacturing_worksheet(manufactured_data)

    available_stock()

print('Welcome to the EPC Production Schedule \n')
main()

