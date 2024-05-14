import gspread
from tabulate import tabulate
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("EPC_Production_Schedule")

black = "\033[0;30m"
red = "\033[0;31m"
green = "\033[0;32m"
yellow = "\033[0;33m"
white = "\033[0;37m"
nocolor = "\033[0m"
bold = "\033[1m"
underline = "\033[4m"
background_color = "\033[105m"
clearscreen = "\033[H\033[J]"
bigger = "\033[4;1m"
reset = "\033[0m"


def get_sales_figures():
    """
    function to get sales data for the salesPerDay sheet
    """
    while True:
        print("Please enter sales per day for each production line.")
        print("Sales figures should be entered as 5 numbers," " separated by commas.\n")
        sales_data = input(f"{yellow}𝐸𝑛𝑡𝑒𝑟 𝑦𝑜𝑢𝑟 𝑠𝑎𝑙𝑒𝑠 𝑑𝑎𝑡𝑎 ℎ𝑒𝑟𝑒:{white}\n")
        sales_numbers = sales_data.split(",")
        if validate_data(sales_numbers):
            return sales_numbers
        else:
            print(f"{red}Invalid data: Please try again.{white}\n")


def get_lineOutput_figures():
    """
    function to get the unit output data for the lineOutput sheet
    """
    while True:
        print("Please enter line output numbers per day.")
        print(
            "Line Output figures should be entered as 5 numbers,"
            "separated by commas.\n"
        )
        line_output_data = input(f"{yellow}𝐸𝑛𝑡𝑒𝑟 𝑦𝑜𝑢𝑟 𝑙𝑖𝑛𝑒 𝑜𝑢𝑡𝑝𝑢𝑡 𝑑𝑎𝑡𝑎 ℎ𝑒𝑟𝑒:{white}\n")
        output_numbers = line_output_data.split(",")
        # To check the validate function against the data
        if validate_data(output_numbers):
            return output_numbers
        else:
            print(f"{red}Invalid data: Please try again.{white}\n")


def get_manufactured_figures():
    """
    function to get the manufactured volume data for the
    manufacturedVolume sheet
    """
    while True:
        print("Please enter Manufactured Volume .")
        print(
            "Manufactured Volume figures should be"
            "entered as 5 numbers, separated by commas."
            "If nothing was manufactured, enter zero.\n"
        )
        manufactured_volume_data = input(
            f"{yellow}𝐸𝑛𝑡𝑒𝑟 𝑦𝑜𝑢𝑟 𝑚𝑎𝑛𝑢𝑓𝑎𝑐𝑡𝑢𝑟𝑖𝑛𝑔 𝑑𝑎𝑡𝑎 ℎ𝑒𝑟𝑒:{white}\n"
        )
        volume_numbers = manufactured_volume_data.split(",")
        if validate_data(volume_numbers):
            return volume_numbers
        else:
            print(f"{red}Invalid data: Please try again.{white}\n")


def validate_data(values):
    """
    Validation function to ensure that the data type entered is 5
    in length and are integers
    """
    try:
        if len(values) != 5 or not all(value.isdigit() for value in values):
            raise ValueError(
                f"{red}Please enter 5 whole numbers separated by commas,"
                "you entered:{white} {values}"
            )
        return True
    except ValueError as e:
        print(f"{red}Invalid data: {e}, please try again.{white}\n")
        return False


def update_sales_worksheet(data):
    """
    Function to update the sales worksheet.
    """
    if len(data) == 5 and all(isinstance(num, int) for num in data):
        sales_worksheet = SHEET.worksheet("salesPerDay")
        sales_worksheet.append_row(data)
        print(f"{green}Sales worksheet updated successfully{white}\n")
    else:
        print(
            f"{red}Invalid data format:"
            " Unable to update the sales worksheet.{white}\n"
        )


def update_line_worksheet(data):
    """
    function to update the line output worksheet
    """
    if len(data) == 5 and all(isinstance(num, int) for num in data):
        line_output_worksheet = SHEET.worksheet("lineOutput")
        line_output_worksheet.append_row(data)
        print(f"{green}Line Output worksheet updated successfully{white}\n")
    else:
        print(
            f"{red}Invalid data format:"
            "Unable to update the line Output worksheet.{white}\n"
        )


def update_manufacturing_worksheet(data):
    """
    function to update the manufacturing worksheet
    """
    if len(data) == 5 and all(isinstance(num, int) for num in data):
        manufactured_worksheet = SHEET.worksheet("manufacturedVolume")
        manufactured_worksheet.append_row(data)
        print(f"{green}Manufactured Volume worksheet" f"updated successfully{white}\n")
    else:
        print(
            f"{red}Invalid data format:"
            " Unable to update the Manufactured Volume worksheet.{white}\n"
        )


def available_stock():
    """
    Function to get the lineOutput data and add it to the last line
    of the available stock data and subtract the sales data to give
    an updated available stock data. This gives me available stock
    to work with and an accumulated number.
    """
    line_output_worksheet = SHEET.worksheet("lineOutput")
    available_stock_worksheet = SHEET.worksheet("AvailableStockUnits")
    sales_worksheet = SHEET.worksheet("salesPerDay")

    # To get the last row from the "lineOutput" worksheet
    last_line_output_row = line_output_worksheet.get_all_values()[-1]

    # If there is data in the last row of "lineOutput"
    if last_line_output_row:
        last_line_output_values = [int(num) for num in last_line_output_row]

        # To get the last row from the "AvailableStockUnits" worksheet
        last_available_stock_row = available_stock_worksheet.get_all_values()[-1]

        # When there is data in the last row of the sheet
        if last_available_stock_row:
            last_available_stock_values = [
                int(value) if value.isdigit() else 0
                for value in last_available_stock_row
            ]
        else:
            # When there is no numerical data in the last row of
            # "AvailableStockUnits" worksheet,
            # use the current line output values
            last_available_stock_values = last_line_output_values

        new_row_values = [
            str(output + stock)
            for output, stock in zip(
                last_line_output_values, last_available_stock_values
            )
        ]

        # To get the last row from the "salesPerDay" worksheet
        last_sales_row = sales_worksheet.get_all_values()[-1]

        # If there is data in the last sales row, subtract the sales values
        if last_sales_row:
            last_sales_values = [int(num) for num in last_sales_row]
            new_row_values = [
                str(int(stock) - sales)
                for stock, sales in zip(new_row_values, last_sales_values)
            ]

        # Append the calculated values as a new row to "AvailableStockUnits"
        available_stock_worksheet.append_row(new_row_values)
        print(f"{green}Available Stock updated successfully{white}\n")
    else:
        print(f'{red}Not enough data in the "lineOutput" sheet.{white}')


def days_of_available_stock():
    """
    Function to calculate the amount of finished stock
    that is required to keep ahead of demand.
    Available stock divided by the average of the last 5 days sales.
    """
    sales_per_day_worksheet = SHEET.worksheet("salesPerDay")
    sales_data = sales_per_day_worksheet.get_all_values()
    if len(sales_data) < 5:
        print(
            f"{red}Error: There are fewer than 5 lines of data in the "
            f"'salesPerDay' sheet. Please update salesPerDay sheet{white}\n"
        )
        return
    available_stock_worksheet = SHEET.worksheet("AvailableStockUnits").get_all_values()
    sales_per_day_worksheet = SHEET.worksheet("salesPerDay").get_all_values()
    stock_days_on_hand_worksheet = SHEET.worksheet("AvailableStockDays")
    # Get last line of available stock
    last_line_available_stock = available_stock_worksheet[-1]
    # Convert to an integer
    last_line_available_stock = [int(value) for value in last_line_available_stock]
    # Last 5 days sales
    last_five_rows_sales = sales_per_day_worksheet[-5:]
    # Add the last five days sales together, column totals
    column_totals = [0] * len(last_five_rows_sales[0])
    for row in last_five_rows_sales:
        for i, value in enumerate(row):
            column_totals[i] += int(value)
    [
        int(value)
        for value in SHEET.worksheet("AvailableStockUnits").get_all_values()[-1]
    ]
    # Get the average for the last 5 days
    average_sales_for_last_five_days_sales = [total / 5 for total in column_totals]
    # Get the number of days stock available
    days_of_available_stock = [
        round(last_line_available_stock[i] / average_sales_for_last_five_days_sales[i])
        for i in range(len(last_line_available_stock))
    ]
    # Update the Available Stock Days worksheet
    stock_days_on_hand_worksheet.append_row(days_of_available_stock)
    print(f"{green}Available Stock Days worksheet updated successfully{white}\n")
    return days_of_available_stock


def available_production_stock():
    """
    function to calculate available production stock
    and update the worksheet. It adds the current days
    manufactured stock to the previous days stock and
    subtracts the line output number.
    """
    # Get the manufacturedVolume sheet
    manufactured_stock = SHEET.worksheet("manufacturedVolume").get_all_values()
    lineOuput_stock = SHEET.worksheet("lineOutput").get_all_values()
    # get the last row from the line output sheet
    lineOutput_numbers = [int(num) for num in lineOuput_stock[-1]]
    # Get the last 2 rows from this sheet
    manufactured_stock_last_two_rows = [
        list(map(int, row)) for row in manufactured_stock[-2:]
    ]
    # get the accumulated number of the last two rows of the manufactured stock
    accumulated_manufactured_stock = [
        sum(values) for values in zip(*manufactured_stock_last_two_rows)
    ]
    # Calculate available production stock.
    # Accumulated stock minus line output stock
    available_manufactured_stock = [
        a - b for a, b in zip(accumulated_manufactured_stock, lineOutput_numbers)
    ]
    available_manufactured_numbers = SHEET.worksheet("availableManufacturedVolume")
    available_manufactured_numbers.append_row(available_manufactured_stock)
    print(f"{green}ManufacturedVolume worksheet updated successfully{white}\n")


def total_manufactured_stock_in_days():
    """
    Function to calculate the total amount of manufactured stock in days
    The number of available finished stock units plus the available
    manufactured volume divided by the average of the last 10 days sales
    """
    sales_per_day_worksheet = SHEET.worksheet("salesPerDay")
    sales_data = sales_per_day_worksheet.get_all_values()
    if len(sales_data) < 10:
        print(
            f"{red}Error: There are fewer than 10 lines of data in the "
            f"'salesPerDay' sheet. Please update salesPerDay sheet{white}\n"
        )
        return
    sales_per_day_worksheet = SHEET.worksheet("salesPerDay").get_all_values()
    available_manufactured_volume = [
        int(value)
        for value in SHEET.worksheet("availableManufacturedVolume").get_all_values()[-1]
    ]
    available_finished_stock_units = [
        int(value)
        for value in SHEET.worksheet("AvailableStockUnits").get_all_values()[-1]
    ]
    sales_days_of_all_stock = SHEET.worksheet("salesDaysOfAllManufacturedStock")
    # Last 10 days sales
    last_ten_rows_sales = sales_per_day_worksheet[-10:]
    # Add the last ten days sales together, column totals
    column_totals = [0] * len(last_ten_rows_sales[0])
    for row in last_ten_rows_sales:
        for i, value in enumerate(row):
            column_totals[i] += int(value)
    # Get the average for the last 10 days
    average_sales_for_last_ten_days_sales = [int(total / 10) for total in column_totals]
    # calculation for manufactured stock available in days
    sales_days_of_all_manufactured_stock = [
        int((a + b) / c)
        for a, b, c in zip(
            available_finished_stock_units,
            available_manufactured_volume,
            average_sales_for_last_ten_days_sales,
        )
    ]
    sales_days_of_all_stock.append_row(sales_days_of_all_manufactured_stock)
    print(
        f"{green}Sales days of all manufactured stock"
        f" worksheet updated successfully{white}\n"
    )


def manufacturing_requirment():
    """
    Function to calculate the manufacturing reequirement. It takes
    the number of available finished stock units plus the abailable
    manufactured volume divided by the average of the last 10 days
    sales. If this number is less than 5 it recommends production of
    average of last 10 days sales X 15. This will give a max of 20
    days stock. If the number is greater than 5 it recommends 0 production
    """
    sales_per_day_worksheet = SHEET.worksheet("salesPerDay")
    sales_data = sales_per_day_worksheet.get_all_values()

    # Check if there are fewer than 10 lines of data in the "salesPerDay" sheet
    if len(sales_data) < 10:
        print(
            f"{red}Error: There are fewer than 10 lines of data in the "
            f"'salesPerDay' sheet.{white}\n"
        )
        return
    total_manufactured_stock = [
        int(value)
        for value in SHEET.worksheet(
            "salesDaysOfAllManufacturedStock"
        ).get_all_values()[-1]
    ]
    sales_per_day_worksheet = SHEET.worksheet("salesPerDay").get_all_values()
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
        if column_total[i] < 5:
            column_total[i] += 15 * average_sales_for_last_ten_days_sales[i]
        else:
            column_total[i] = 0
    SHEET.worksheet("ManufacturingStockRequiredVolume").append_row(column_total)
    print(
        f"{green}Manufactured Stock Required Sheet" f"  updated successfully{white}\n"
    )


def dataTable():
    """
    Function to create a table of the data collected
    """
    # create a table for the three sets of input data above
    print(
        f"{red}{underline}{bold}Ｍａｎｕｆａｃｔｕｒｉｎｇ Ｄａｔａ Ｔａｂｌｅ{reset}\n"
    )
    sales_data = [
        int(value) for value in SHEET.worksheet("salesPerDay").get_all_values()[-1]
    ]
    line_output_data = [
        int(value) for value in SHEET.worksheet("lineOutput").get_all_values()[-1]
    ]
    manufactured_volume_data = [
        int(value)
        for value in SHEET.worksheet("manufacturedVolume").get_all_values()[-1]
    ]
    available_stock_data = [
        int(value)
        for value in SHEET.worksheet("AvailableStockUnits").get_all_values()[-1]
    ]
    days_available_stock_data = [
        int(value)
        for value in SHEET.worksheet("AvailableStockDays").get_all_values()[-1]
    ]
    available_production_stock_data = [
        int(value)
        for value in SHEET.worksheet("availableManufacturedVolume").get_all_values()[-1]
    ]
    days_manufactured_stock_data = [
        int(value)
        for value in SHEET.worksheet(
            "salesDaysOfAllManufacturedStock"
        ).get_all_values()[-1]
    ]
    manufacturing_requirement_data = [
        int(value)
        for value in SHEET.worksheet(
            "ManufacturingStockRequiredVolume"
        ).get_all_values()[-1]
    ]
    # create the header tags
    headers = [
        f"{yellow}{bold}Line1{reset}",
        f"{yellow}{bold}Line2{reset}",
        f"{yellow}{bold}Line3{reset}",
        f"{yellow}{bold}Line4{reset}",
        f"{yellow}{bold}Line5{reset}",
    ]
    # create the y axis labels
    table_data = [
        [f"{yellow}{bold}Sales{reset}"] + sales_data,
        [f"{yellow}{bold}Line Output{reset}"] + line_output_data,
        [f"{yellow}{bold}Manufactured Volume{reset}"] + manufactured_volume_data,
        [f"{yellow}{bold}Available Stock{reset}"] + available_stock_data,
        [f"{yellow}{bold}Days of Available Stock{reset}"] + days_available_stock_data,
        [f"{yellow}{bold}Available Production Stock{reset}"]
        + available_production_stock_data,
        [f"{yellow}{bold}Days of Manufactured Stock{reset}"]
        + days_manufactured_stock_data,
        [f"{yellow}{bold}Manufacturing Requirement{reset}"]
        + manufacturing_requirement_data,
    ]
    # print the table
    print(tabulate(table_data, headers, tablefmt="grid"))
    print()
    print()


def available_stock_graph():
    """
    Function to create a graph of the available stock data
    """
    print(f"{red}{bold}{underline}Ａｖａｉｌａｂｌｅ Ｓｔｏｃｋ Ｇｒａｐｈ{reset}\n")
    # data is the output data from days_of_available stock
    data = SHEET.worksheet("AvailableStockUnits").get_all_values()[-1]
    data = [int(value) for value in data]
    # find the max data in the list
    max_value = max(data)
    increment = max_value / 25
    # empty array
    output_lines = []
    # for loop
    for idx, count in enumerate(data):
        # work out the bar chart
        bar_chunks, remainder = divmod(int(count * 8 / increment), 8)
        # create the bar
        bar = "█" * bar_chunks
        # give the remainder if the bar is not a full increment
        if remainder > 0:
            bar += chr(ord("█") + (8 - remainder))
        # use if the bar is empty
        bar = bar or "▏"
        # label for lines
        output_lines.append(
            f"{yellow}{bold}{underline}"
            f"Production line {idx+1}{reset} ▏ {count:#4d} {bar}"
        )
    # label for y-axis
    print()
    # write the output lines to a text file
    # so will work when deployed to heroku
    with open("graph_output.txt", "w", encoding="utf-8") as file:
        for line in output_lines:
            file.write(line + "\n")
    # read and print the file so it shows when deployed
    with open("graph_output.txt", "r", encoding="utf-8") as file:
        print(file.read())


def main():
    """
    Main function to contain all functions
    """
    # https://fsymbols.com/generators/smallcaps/
    print(
        f"{red}{bold}{bigger}ＥＰＣ Ｐｒｏｄｕｃｔｉｏｎ Ｓｃｈｅｄｕｌｅｒ.{white}\n"
    )

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
    available_stock_graph()


if __name__ == "__main__":

    main()
