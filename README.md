### EPC Manufacturing Scheduler
(By Declan Lenahan)

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/39ff2aa5-6c6f-42b8-8466-42aba9b5ec07)


This project was based on the production requirement, particularly the manufacturing requirement that would be needed when running five filling lines. This is an area that I have lots of experience in and when building this program it was something that I would have liked to have when I was planning my production. The objective or the program is to is to get three sets of input from the user, 
1.  unit sales per line,
2.  the line output for each line
3.  the amount of product for each line that was manufactured.

Each of these figures are entered by the user on a daily basis. The data entered is validated before it is accepted to be uploaded to google docs.  
The program then takes this information and feeds to a google docs spreadsheet which is connected to the program, and claculates the following:
1.   Available Stock units - the amount of finished units i.e. post production line output
2.   Available Stodk units in days - this is this unit figure divided by the average of 5 days sales
3.  The available Manufactured Volume - this is the current days manufactured stock added to the previous days available manufactured stock and     then subtracts the line output number.
4.  Sales Day of all Manufactured Stock - this is a function to calculate the total amount of manufactured stock in days which is the         number of available finished stock units plus the available manufactured volume divided by the average of the last 10 days sales.
5.  Manufacturing Stock Requirement Volume - this is a function to calculate the manufacturing reequirement. It takes the number of           available finished stock units plus the abailable manufactured volume divided by the average of the last 10 days sales. If this           number is less than 5 it recommends production of average of last 10 days sales X 15. This will give a max of 20 days stock. If the       number is greater than 5 it recommends 0 production.
  
This caused me no end of trouble when I ran a factory as your sales per unit is a number of points away  from manufacturing and this program allows the two to be connected through the calculations. With this I mean that sales would increase and the availabe stock would be in the warehouse but this would not filter down to the manufacturing floor and when it did, manufactuing were trying to catch up. This program, links the sales per day to the manufacturing requirement which is of vital importance when running a manufacturing and sales company.

As this program needs 10 days of sales data to be entered into the spreadsheet, I have set a function to ask the user if this is the case. I it is y, then the user can progress, if n then the user is requested to enter the data into the spreadsheet and when done they can answer y and progress. I have created a validation function to check if there is 10 rows of data and that the data is an integer. If not the user is prompted to enter the data in the salesPerDay worksheet again. This ensures that 10 rows of data has been entered into the spreadsheet. I have also included error messages within the functions needing to use the sales data as a secondary safety measure to ensure that this has been done.

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/44a9b967-5676-40d8-86bf-6a7522462610)

The user is then requested to enter the data for sales, line output and manufacturing output. They are instructed to enter 5 numbers separated by commas. This is the data that is entered onto the spreadsheet. If the data entered is not in this exact format then the program shows an error and asks the user to input the correct data.

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/cbdeee66-2056-424e-b491-35b8ba56aecd)

I have included statements showing that each of the sheets have been updated successfully. Again if this did not happen a message to the user would be sent to say that it was unsucessful due to invalid format. In the real world, I would leave this out and the program would just go to the table and graph.

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/df0e9549-7697-44bb-bc19-3f35bcdbf36b)
 

The data is then presented in a table format and a graph format for ease of viewing.

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/1ec86378-7a81-4cb9-8fd5-bf8f16b3e80f)



![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/94a72ac9-3070-4114-8e5f-4f4fbfb2e13d)

## Lucidchart

![Flowcharts (2)](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/ca4aebe0-e412-4339-ba2e-dcea91d2c2d1)


## Deployment

Code Institute Python Essentials Template was used for this project so the python code can be viewed in a terminal in a browser:
1. Google Heroku and open website, log in to Heroku or create a new account
2. On the dashboard click "New" and select "Create new app"
3. Enter unique app name and select region
4. Click "Create app"
5. On the next page find "Settings" tab and locate "Config Vars"
6. Click "Reveal Config Vars" and add "PORT" as a key and with value "8000", click "Add"
7. Scroll down to "Buildpack" and click "Add", select "Python" first
8. Repeat step 7. to add "Node.js", making sure "Python" is first on the list
9. Scroll to the top and select "Deploy" tab
10. Select GitHub as deployment method and search for your repository, once found click "Connect"
11. Scroll down and choose between "Enable Automatic Deploys" so the code is updated every time it is pushed to Github or "Manual Deploy"
Deployed site accesible (https://epcproductionscheduler-056411610085.herokuapp.com/)



## Testing

I have tested the program on my own system and some others with no issues. My mentor has also run the program on his system with no issues. When running the program, if less than 10 rows of data was contained in the sales sheet, the program gave an error. This was fixed by asking the user if 10 rows of data has been entered in the sales sheet and if not, they are not allowed to continue. I have also included an  error handling messages to ask the user to input the appropriate data in the spreadsheet within each of the functions that require the average sales number. 

I have tested the program with zero data in all sheets except the sales sheet which again was causing errors but these are now fixed. 
for a, b, c in zip(
            available_finished_stock_units,
            available_manufactured_volume,
            average_sales_for_last_ten_days_sales):
This zip code was causing a problem as if a or be were zero then to divide zero by a number was causing an error. I fixed this with the addition of the following 
        if a + b == 0:
            sales_days_of_all_manufactured_stock.append(0) 

As the program looks for the last row of data, and in this case the last row could be the headings row which are non integers, this also was causing problems. To solve this I ensured that any data that was accepted had to be an integer.
last_line_available_stock = [int(value) for value in last_line_available_stock]

I used is isdigit() else 0 to ensure that if the row was empty that it was converted to an integer 0. This solved alot of errors that were caused when I ran an empty sheet.

last_available_stock_row:
            last_available_stock_values = [
                int(value) if value.isdigit() else 0
                for value in last_available_stock_row
            ]
        else:
            # When there is no numerical data in the last row of
            # "availableManufacturedVolume" worksheet,
            # use the current manufacturedVolume values
            last_available_stock_values = last_line_manufactured_values

As 3 of the functions needed a minimum of 10 rows of data and this was causing errors I decided to include a function validate_sales_data at the start of the program to check if the data had been entered even if the user types y when asked. This function also checks if the data are integers and there is at least 10 rows. This ensures from the start of the program that the data is in the sheet and correct. The funtion will not let the user progress unless all correct data is in the sheet.

## Testing in linter

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/e6b47ea6-ed33-425c-af74-266715df397c)


## Future Developments

This program has so many future features and developments that could be added. Ideally it would be run through an interface that allowed the user to enter the data. This interface could also allow the user to alter other variables like the number of days to work out the average sales per day and to set the upper and lower limits of when to manufacture and how much to manufacture. This program could also be linked to a raw material procurement system to allow prediction of purchase of raw materials needed for manufacture. The possibilities are endless hence why I will develop this program more or something like it when I get more advanced in this course and have more knowledge. 

## Error Handling

The sales input sheet needs to be pre-populated with 10 days sales to enable the program to get its average as three functions call for a 5 day average and a 10 day average of sales. 
The available stock units sheet needs to be populated with one line of data. 
Error handling messages have been included within the functions that prompt the user to populate the sales sheet in the event that there is inadequate data available.
The validate_sales_data also contains error handling messages to ensure that the correct data and quantity is in the salesPerDay sheet.

## Link to Google Sheets

https://docs.google.com/spreadsheets/d/1QbLNmzxHJjRSDZsKfbWj7dfg46BbJ5_cJfqDzHWjsSI/edit#gid=1787962955

## Acknowledgements and Credits

I'd like to thank Spencer Barriball, my mentor at Code Institute, for giving me valuable guidance and support throught the duration of this project. Excellent advice and direction. 
I got the inspiration from the Love Sandwiches project and then elaborated on this model. This was definately my starting point and the learning from that walkthrough got me started along this path. 
For the generation of the colours i used the link below:
https://code-maven.com/ansi-command-line-colors-with-python
For the generation of the different fonts i used the link below:
https://fsymbols.com/generators/smallcaps/
I have used gspread, tabulate and google.oath.
The program is linked to google docs which contains all the data.
I used the learning from the link below to create the table using tabulate:
https://www.statology.org/create-table-in-python/
I used w3schools for the use of zip https://www.w3schools.com/python/ref_func_zip.asp.
I used w3schools for the use of range https://www.w3schools.com/python/ref_func_range.asp.
I used https://alexwlchan.net/2018/ascii-bar-charts/ as my learning for building the bar chart.
I used https://www.geeksforgeeks.org/enumerate-in-python/ to understand the enumerate function

I tried so many ways to try to create a graph but as this had to be prompt based I had to settle on the method used which saves to the graph_output.text file and this is what worked with heroku.

I have reviewed hours and hours of videos, text learning and course learning to generate this program. 
All the code with the exceptions of any mentions above were generated by myself. 




