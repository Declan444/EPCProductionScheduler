EPC Manufacturing Planner
![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/cbdeee66-2056-424e-b491-35b8ba56aecd)

This project was based on the production requirement, particularly the manufacturing requirement that would be needed when running five filling lines. This is an area that I have lots of experience in and when building this program it was something that I would have liked to have when I was planning my production. The objective is to get three sets of input from the user, unit sales per line, the line output for each line and the amount of product for each line that was manufactured. Each of these figures are entered by the user on a daily basis. The data entered is validated before it is accepted to be uploaded to the google docs.  The program then takes this information and feeds to a google docs spreadsheet which is connected to the program, and a range of functions manipulate the entered data to populate a number of other sheets contained within the google docs. The google docs sheet contains sheets to catch the data that is generated in each of the functions by using the input data. The program works out the amount of available manufactured stock in units and the amount of manufactured stock in days, days being an average of the last 10 days sales, it works out the available stock in units and how that converts to sales days. It uses all of this information to suggest a manufacturing volume that needs to be manufactured to ensure that the manufactured stock meets the requirements of each line so that the lines can output finished commercial product. The program checks the data and when all of the manufactured stock is less than 5 days of sales, the program recommends the production of 15 days stock converted to units by multiplying by the average of the last 10 days of sales. This ensures that manufacturing is ahead of the demand. 

This caused me no end of trouble when I ran a factory as your sales per unit is a number of points away  from manufacturing and this program allows the two to be connected through the calculation. 


![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/aededa87-c4d7-4954-9395-5f9bc91e5f5e)

![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/94a72ac9-3070-4114-8e5f-4f4fbfb2e13d)

## Lucidchart
![image](https://github.com/Declan444/EPCProductionScheduler/assets/119152450/a1149479-7c93-41ef-840b-4eaf441b5b99)


## Deployment
Deploying to Heroku
Code Institute Python Essentials Template was used for this project so the python code can be viewed in a terminal in a browser:

Google Heroku and open website, log in to Heroku or create a new account
On the dashboard click "New" and select "Create new app"
Enter unique app name and select region
Click "Create app"
On the next page find "Settings" tab and locate "Config Vars"
Click "Reveal Config Vars" and add "PORT" as a key and with value "8000", click "Add"
Scroll down to "Buildpack" and click "Add", select "Python" first
Repeat step 7. to add "Node.js", making sure "Python" is first on the list
Scroll to the top and select "Deploy" tab
Select GitHub as deployment method and search for your repository, once found click "Connect"
Scroll down and choose between "Enable Automatic Deploys" so the code is updated every time it is pushed to Github or "Manual Deploy"
Deployed site accesible through this link Dragons


- Your code must be placed in the `run.py` file
- Your dependencies must be placed in the `requirements.txt` file
- Do not edit any of the other files or your code may not deploy properly

## Future Developments
This program has so many future features and developments that could be added. Ideally it would be run through an interface that allowed the user to enter the data. This interface could also allow the user to alter other variables like the number of days to work out the average sales per day and to set the upper and lower limits of when to manufacture and how much to manufacture. This program could also be linked to a raw material procurement system to allow prediction of purchase of raw materials needed for manufacture. The possibilities are endless hence why I will develop this program more or something like it when I get more advanced in this course and have more knowledge. 

## Acknowledgements and Credits



