# Cath's Cats' Castle - booking
## Screenshot ???

link to live page [here]()



## Aim of the website

## Structure of the website


## Features



## Styling


## Bugs
1. Issue with accessing data needed to update both worksheets. Each set of data: dates, email, room number were local variables in the new booking function. Managed to pass various variables to the functions so each value is read correctly.

2. Issue with Rooms Worksheet - recording new booking - new booking was not apearing in the apropriate column for the room. Found that data is saved under identical column number as it is saved in clients worksheet. Found function that was refering to clients worksheet and replaced it with variable worksheet. Worksheet wariable had the appropriate worksheet passed to it when the function was called and the correct column in the rooms worksheet was updated.

3. Issue with lenght of the line:
- the errors were raised in the lines where the if statement was very long. followed advice from [stack overflow](https://stackoverflow.com/questions/5253348/very-long-if-statement-in-python)
- the error with very long regex - I left it untouched as I am concerned that it would stop working

4. Bug caused by is_empty_cell function. The function was supposed to test if the cell is empty, I tried to use it both for validation of new booking as well as cancellation of the existing booking. There logic was incorrect and I created the seperate function to is_full_cell - to test if all cells are full. 

5. Bug in deleting the booking from the spreadsheet. 
    - the user inputs the dates for cancelation. The dates are validated
    - the program checks what was the room name on the first date within cancelation period in the clients spreadsheet
    - the program deletes the booking from the rooms spreadsheet on the basis of what room was within the first day of booking
    - the assumption is that the client will book a longer period of time in the same room, he will not change rooms
    - I tried to capture the room name from the clients spreadsheet, which introduced a new bug, which I have not been managed to fix,
    - I reversed to the version of the function that assumes that the room that is being cancelled is the same for the whole cancelation period
6. Double booking
Program only checks if the room is available on those dates, it can over ride the entries of old booking under the client's email and add an new booking in a different room. The client would end up having 2 rooms booked in the same time, but only the most recent room would display under his name.
  
## Validation



## Previous project (to be deleted)



## Further developement the website


## User stories



## Technologies used


## Thanks to


## Joanna - remember to find all ??? signs in all files (readme as well)




![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

Welcome Joanna Gorska,

This is the Code Institute student template for deploying your third portfolio project, the Python command-line project. The last update to this file was: **August 17, 2021**

## Reminders


* Terminal of 80 characters wide and 24 rows high

* Your code must be placed in the `run.py` file
* Your dependencies must be placed in the `requirements.txt` file
* Do not edit any of the other files or your code may not deploy properly

## Creating the Heroku app

When you create the app, you will need to add two buildpacks from the _Settings_ tab. The ordering is as follows:

1. `heroku/python`
2. `heroku/nodejs`

You must then create a _Config Var_ called `PORT`. Set this to `8000`

If you have credentials, such as in the Love Sandwiches project, you must create another _Config Var_ called `CREDS` and paste the JSON into the value field.

Connect your GitHub repository and deploy as normal.

## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

-----
Happy coding!