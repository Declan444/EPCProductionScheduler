### EPC Manufacturing Scheduler
(By Declan Lenahan)

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/cbdeee66-2056-424e-b491-35b8ba56aecd)

This project was based on the production requirement, particularly the manufacturing requirement that would be needed when running five filling lines. This is an area that I have lots of experience in and when building this program it was something that I would have liked to have when I was planning my production. The objective or the program is to is to get three sets of input from the user, 
1.  unit sales per line,
2.  the line output for each line
3.  the amount of product for each line that was manufactured.

Each of these figures are entered by the user on a daily basis. The data entered is validated before it is accepted to be uploaded to google docs.  
The program then takes this information and feeds to a google docs spreadsheet which is connected to the program, and claculates the following:
1.   Available Stock units - the amount of finished units i.e. post production line output
2.   Available Stodk units in days - this is this unit figure divided by the average of 5 days sales
3.  The available Manufactured Volume - this is the current days manufactured stock to the previous days available manufactured stock and     then subtracts the line output number.
4.  Sales Day of all Manufactured Stock - this is a function to calculate the total amount of manufactured stock in days which is the         number of available finished stock units plus the available manufactured volume divided by the average of the last 10 days sales.
5.  Manufacturing Stock Requirement Volume - this is a function to calculate the manufacturing reequirement. It takes the number of           available finished stock units plus the abailable manufactured volume divided by the average of the last 10 days sales. If this           number is less than 5 it recommends production of average of last 10 days sales X 15. This will give a max of 20 days stock. If the       number is greater than 5 it recommends 0 production.
  
This caused me no end of trouble when I ran a factory as your sales per unit is a number of points away  from manufacturing and this program allows the two to be connected through the calculations. 

The data is then presented in a table format and a graph format for ease of viewing.


![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/aededa87-c4d7-4954-9395-5f9bc91e5f5e)

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/94a72ac9-3070-4114-8e5f-4f4fbfb2e13d)

## Lucidchart

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/a1149479-7c93-41ef-840b-4eaf441b5b99)


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

I have tested the program on my own system and some others with no issues. My mentor has also run the program on his system with no issues. When running the program, if less than 10 rows of data was contained in the sales sheet, the program gave an error. This was fixed by including error handling messages to ask the user to input the appropriate data in the spreadsheet. As available stock uses two lines data, this also gave an error if there was no data in the sheet. As the first line of data in the sheet are the sheet headings, it was a persistant error. This was fixed by checking only if a numerical value was present, and if not then to use the line output value as the first line of data for the available stock sheet. This solved this error.

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/e6b47ea6-ed33-425c-af74-266715df397c)


## Future Developments

This program has so many future features and developments that could be added. Ideally it would be run through an interface that allowed the user to enter the data. This interface could also allow the user to alter other variables like the number of days to work out the average sales per day and to set the upper and lower limits of when to manufacture and how much to manufacture. This program could also be linked to a raw material procurement system to allow prediction of purchase of raw materials needed for manufacture. The possibilities are endless hence why I will develop this program more or something like it when I get more advanced in this course and have more knowledge. 

## Error Handling

The sales input sheet needs to be pre-populated with 10 days sales to enable the program to get its average as three functions call for a 5 day average and a 10 day average of sales. 
The available stock units sheet needs to be populated with one line of data. 
Error handling messages have been included within the functions that prompt the user to populate the sales sheet in the event that there is inadequate data available.

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

I tried so many ways to try to create a graph but as this had to be prompt based I had to settle on the method used which saves to the graph_output.text file and this is what worked with heroku.

I have reviewed hours and hours of videos, text learning and course learning to generate this program. 
All the code with the exceptions of any mentions above were generated by myself. 




