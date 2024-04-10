import gspread
from tabulate import tabulate

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

black   = "\033[0;30m"
red     = "\033[0;31m"
green   = "\033[0;32m"
yellow  = "\033[0;33m"
white   = "\033[0;37m"
nocolor = "\033[0m"
bold = '\033[1m'
underline = '\033[4m'
background_color = '\033[105m'
clearscreen = '\033[H\033[J]'
bigger = '\033[4;1m'
reset = '\033[0m'

def get_sales_figures():
    """function to get sales data for the salesPerDay sheet """
    while True:
        print('Please enter sales per day for each line.')
        print('Sales figures should be entered as 5 numbers, separated by commas.\n')
    
        
        sales_data = input(f'{yellow}Enter your data here:{white}\n')
        sales_numbers = sales_data.split(',')
        
        if validate_data(sales_numbers):
            print('Numbers Validated', sales_numbers)
            
            return sales_numbers
        else:
            print(f'{red}Invalid data: Please try again.{white}\n')

def get_lineOutput_figures():
    """function to get the unit output data for the lineOutput sheet """
    while True:
        print('Please enter line output numbers per day.')
        print('Line Output figures should be entered as 5 numbers, separated by commas.\n')
    
    
        line_output_data = input('Enter your data here:\n')
        output_numbers = line_output_data.split(',')
        # To check the validate function against the data
        if validate_data(output_numbers):
            print('Numbers Validated', output_numbers)
            return output_numbers
        else:
            print('Invalid data: Please try again.\n')

def get_manufactured_figures():
    """function to get the manufactured volume data for the manufacturedVolume sheet """
    while True:
        print('Please enter Manufactured Volume .')
        print('Manufactured Volume figures should be entered as 5 numbers, separated by commas. If nothing was manufactured, enter zero.\n')
    
    
        manufactured_volume_data = input('Enter your data here:\n')
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
    print('Updating line output worksheet....\n')
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

    # If there is data in the last row, convert the values to integers
    if last_line_output_row:
        
        last_line_output_values = [int(num) for num in last_line_output_row]

        # To get the last row from the "AvailableStockUnits" worksheet
        last_available_stock_row = available_stock_worksheet.get_all_values()[-1]

        # When there is data in the last row of the sheet, then add the corresponding values
        #w3schools.com for the use of zip() to accumulate number.
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
            
            new_row_values = [str(int(stock) - sales) for stock, sales in zip(new_row_values, last_sales_values)]

       
        available_stock_worksheet.append_row(new_row_values)
        print('Available Stock updated successfully\n')
        print(new_row_values)
    else:
        print('Not enough data in the "lineOutput" sheet.')
   
    
def days_of_available_stock(): 
    """
    To calculate the amount of finished stock that is required to keep ahead of demand. Available stock divided by the average of the last 5 days sales. 
    """
    available_stock_worksheet = SHEET.worksheet('AvailableStockUnits').get_all_values()
    sales_per_day_worksheet = SHEET.worksheet('salesPerDay').get_all_values()
    stock_days_on_hand_worksheet = SHEET.worksheet('AvailableStockDays')
    # Get last line of available stock
    last_line_available_stock = available_stock_worksheet[-1]
    #Convert to an integer
    last_line_available_stock = [int(value) for value in last_line_available_stock]
    
    # Last 5 days sales
    last_five_rows_sales = sales_per_day_worksheet[-5:]
    # Add the last five days sales together, column totals
    column_totals = [0] * len(last_five_rows_sales[0])
    for row in last_five_rows_sales:
        for i, value in enumerate(row):
            column_totals[i] += int(value)

    [int(value) for value in SHEET.worksheet('AvailableStockUnits').get_all_values()[-1]]
    # Get the average for the last 5 days 
    average_sales_for_last_five_days_sales = [total / 5 for total in column_totals] 

    # Get the number of days stock available
    days_of_available_stock = [round(last_line_available_stock[i] / average_sales_for_last_five_days_sales[i]) for i in range(len(last_line_available_stock))]   

    print('Updating Available Stock Days worksheet....\n')
    # Update the Available Stock Days worksheet    
    stock_days_on_hand_worksheet.append_row(days_of_available_stock)
    print('Available Stock Days worksheet updated successfully\n')
    
    
    print(green)
    print('Number of days available stock:')
    print(white)
    print(days_of_available_stock)
    return days_of_available_stock



def available_production_stock():
    #Get the manufacturedVolume sheet
    manufactured_stock = SHEET.worksheet('manufacturedVolume').get_all_values()
    lineOuput_stock = SHEET.worksheet('lineOutput').get_all_values()
    #get the last row from the line output sheet
    lineOutput_numbers = [int(num) for num in lineOuput_stock[-1]]
    print('LineOutput Last Row Numbers:')
    print(lineOutput_numbers)

    #Get the last 2 rows from this sheet 
    manufactured_stock_last_two_rows = [list(map(int, row)) for row in manufactured_stock[-2:]]

    
    #get the accumulated number of the last two rows of the manufactured stock
    accumulated_manufactured_stock = [sum(values) for values in zip(*manufactured_stock_last_two_rows)]
    print('Available Manufactured Stock:')
    print(accumulated_manufactured_stock)

    #Calculate available production stock. Accumulated stock minus line output stock

    available_manufactured_stock = [a - b for a, b in zip(accumulated_manufactured_stock, lineOutput_numbers)]
    print('Available Manufactured Stock minus lineOutput numbers:')
    print(available_manufactured_stock)
    

    print('Updating AvailableManufacturedVolume worksheet.....')
    available_manufactured_numbers = SHEET.worksheet('availableManufacturedVolume')
    available_manufactured_numbers.append_row(available_manufactured_stock)


    print('AvailableManufacturedVolume worksheet updated successfully')


def total_manufactured_stock_in_days():
    sales_per_day_worksheet = SHEET.worksheet('salesPerDay').get_all_values()
    available_manufactured_volume = [int(value) for value in SHEET.worksheet('availableManufacturedVolume').get_all_values()[-1]]
    available_finished_stock_units = [int(value) for value in SHEET.worksheet('AvailableStockUnits').get_all_values()[-1]]
    sales_days_of_all_stock = SHEET.worksheet('salesDaysOfAllManufacturedStock')
    
     # Last 10 days sales
    last_ten_rows_sales = sales_per_day_worksheet[-10:]
    # Add the last ten days sales together, column totals
    column_totals = [0] * len(last_ten_rows_sales[0])

    for row in last_ten_rows_sales:
        for i, value in enumerate(row):
            column_totals[i] += int(value)
    # Get the average for the last 10 days 
    average_sales_for_last_ten_days_sales = [int(total / 10) for total in column_totals] 
    print('Sales in last 10 rows from the sales sheet')
    print(average_sales_for_last_ten_days_sales)

    print('Last row in available Manufactured Volume')
    print(available_manufactured_volume)

    print('Last row of available Stock Units sheet')
    print(available_finished_stock_units)
    
    # calculation for manufactured stock available in days
    sales_days_of_all_manufactured_stock = [int((a+b) / c) for a, b, c in zip(available_finished_stock_units, available_manufactured_volume, average_sales_for_last_ten_days_sales)]

    print('Sales days in available manufactured stock')
    print(sales_days_of_all_manufactured_stock)

    print('Updating Sales Days of all Manufactured Stock Sheet......')
    sales_days_of_all_stock.append_row(sales_days_of_all_manufactured_stock)
    print('Sales days of all manufactured stock worksheet updated')




def manufacturing_requirment():
    total_manufactured_stock = [int(value) for value in SHEET.worksheet('salesDaysOfAllManufacturedStock').get_all_values()[-1]]
    sales_per_day_worksheet = SHEET.worksheet('salesPerDay').get_all_values()
    
    
     # Last 10 days sales
    last_ten_rows_sales = sales_per_day_worksheet[-10:]
    # Add the last ten days sales together, column totals
    column_totals = [0] * len(last_ten_rows_sales[0])

    for row in last_ten_rows_sales:
        for i, value in enumerate(row):
            column_totals[i] += int(value)
    # Get the average for the last 10 days 
    average_sales_for_last_ten_days_sales = [int(total / 10) for total in column_totals]
    
    column_total = [0] * len(total_manufactured_stock)

    for i, value in enumerate(total_manufactured_stock):
        column_total[i] += value


    for i in range(len(column_total)):
        if column_total[i] <15:
            column_total[i] += 15 * average_sales_for_last_ten_days_sales[i]

        
        
        else:
            column_total[i] = 0

    

    
    print('Manufacturing Stock Requirement:')
    print(column_total)
    print('updating Manufacturing Stock Required Volume Sheet....')
    SHEET.worksheet('ManufacturingStockRequiredVolume').append_row(column_total)
    print('Manufactured Stock Required Sheet updated')



def dataTable():
    #create a table for the three sets of input data above
    sales_data = [int(value) for value in SHEET.worksheet('salesPerDay').get_all_values()[-1]]
    line_output_data = [int(value) for value in SHEET.worksheet('lineOutput').get_all_values()[-1]]
    manufactured_volume_data = [int(value) for value in SHEET.worksheet('manufacturedVolume').get_all_values()[-1]]
    available_stock_data = [int(value) for value in SHEET.worksheet('AvailableStockUnits').get_all_values()[-1]]
    days_available_stock_data = [int(value) for value in SHEET.worksheet('AvailableStockDays').get_all_values()[-1]]
    available_production_stock_data = [int(value) for value in SHEET.worksheet('availableManufacturedVolume').get_all_values()[-1]]
    days_manufactured_stock_data = [int(value) for value in SHEET.worksheet('salesDaysOfAllManufacturedStock').get_all_values()[-1]]
    manufacturing_requirement_data = [int(value) for value in SHEET.worksheet('ManufacturingStockRequiredVolume').get_all_values()[-1]]
    #create the header tags
    headers = ['Line1', 'Line2', 'Line3', 'Line4', 'Line5']
    #create the y axis labels
    table_data =[
        ['Sales'] + sales_data, 
        ['Line Output'] + line_output_data,  

        ['Manufactured Volume'] + manufactured_volume_data,
        ['Available Stock'] + available_stock_data,
        ['Days of Available Stock'] + days_available_stock_data,
        ['Available Production Stock'] + available_production_stock_data,
        ['Days of Manufactured Stock'] + days_manufactured_stock_data,
        ['Manufacturing Requirement'] + manufacturing_requirement_data
        ]
    #print the table 
    print(tabulate(table_data, headers, tablefmt='grid')) 

    
def production_requirement_graph():
    # data is the output data from days_of_available stock
    data = SHEET.worksheet('AvailableStockUnits').get_all_values()[-1]

    data = [int(value) for value in data]
    #find the max data in the list
    max_value = max(data)

    increment = max_value / 25

    longest_label_length = len('days')
    #empty array
    output_lines = []
    #for loop
    for idx, count in enumerate(data):
        #work out the bar chart
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)

        #create the bar
        bar = '█' * bar_chunks

    #give the remainder if the bar is not a full increment
        if remainder > 0:
            bar += chr(ord('█') + (8 - remainder))

    #use if the bar is empty
        bar = bar or '▏'
        #label for lines
        output_lines.append(f'Production line{idx+1} ▏ {count:#4d} {bar}')

    #label for y-axis
    output_lines.append(f'{"Available Stock".rjust(longest_label_length)}')

    # write the output lines to a text file so will work when deployed to heroku
    with open('graph_output.txt', 'w', encoding='utf-8') as file:
        for line in output_lines:
            file.write(line + '\n')

    #read and print the file so it shows when deployed
    with open('graph_output.txt', 'r', encoding='utf-8') as file:
        print(file.read())


def main():

    print(f'{red}{bold}{bigger}EPC Production Planner.{white}\n')


    data = get_sales_figures()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    
    lineData = get_lineOutput_figures()
    line_data = [int(num) for num in lineData]
    update_line_worksheet(line_data)

    manufacturedData = get_manufactured_figures()
    manufactured_data = [int(num) for num in manufacturedData]
    update_manufacturing_worksheet(manufactured_data)

    available_stock()
    days_of_available_stock()
    available_production_stock()
    total_manufactured_stock_in_days()
    manufacturing_requirment()
    dataTable()
    production_requirement_graph()
    
if __name__ == "__main__":
    #simple_graph(x,y)
    #https://code-maven.com/ansi-command-line-colors-with-python

    

    main()










