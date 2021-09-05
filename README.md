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