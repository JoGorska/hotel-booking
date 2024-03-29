# Cath's Cats' Castle - booking
## Screenshot 

[![showpiece start screen](assets/images/showpiece.png)](https://hotel-booking-r6x7.onrender.com/)


link to live page [here](https://hotel-booking-r6x7.onrender.com/)


## Aim of the program

This python script was created to complete Project 3 in the Code Institute full stack course. This project is build on the provide template that allows to run a terminal in the browser. 

The aim of the website is to allow users to book their cats' stay in the fictitious cattery called Cath's Cats' castle. 
The project was designed for the purpose of completing Portfolio 3 Project for Diploma in Software Development (E-commerce Applications) with Code Institute

## Structure of the program

The flow chart showing the logic of the program can be found [here](assets/images/flow-chart.png)

The program is a command line program that leads the user through series of questions. 
1. Start
The user is asked for the email
2. The program checks if it is a returning customer
3. The program gives user options to choose from - different options for returning and different for a new customer
    - add - to add a new booking
    - show - to show room's availability
    - print - to print returning user's booking
    - cancel - to cancel returning user's booking
    - change - to change returning user's booking
    - quit - to quit the program

4. When the user wants to action any of the above options he will be asked for
    - start date
    - end date
    - rooms (depending on the option)

5. Once the process is completed - the spreadsheet gets updated with the appropriate action
    - add - adds data to the spreadsheet
    - cancel - removes data from the spreadsheet
    - change - adds and removes data from the spreadsheet

6. After each action, the user is always given returning user options, so he could make another action

7. User can quit the program - when the question to choose the options is displayed.

## Features

1. Images - [ascii art](https://www.asciiart.eu/buildings-and-places/castles)
the image of the castle is shown when the program starts. This gives a nice introduction to the product.
the image of a cat climbing into a box is shown when the program ends. This gives a memorable goodbye to a user.

![castle](assets/images/img-castle.png)


![cat climbing into a box](assets/images/img-cat.png)

2. [Colorama](https://pypi.org/project/colorama/)
added feature to allow different colors of fonts to display in the terminal. This feature aims to help the user understand what the program is doing or what is expected of the user. Since the command-line interface is not user-friendly, the user is not used to read various lines to understand that there was an error returned. Once the error message is in red it stands out amongst other lines and allows the user to act on it. 

While the program is saving things in the spreadsheet it can take a while. The blue lines of code informing the user that the program is saving data help the user to understand that the program is still working, it hasn't broken, it is just taking the time to save data.
- the ValidationErrors are displayed in red
- the positive validation messages are displayed in green
- the information about saving data in the spreadsheet are displayed in blue


![partial screenshoot showing green text in a terminal](assets/images/green.png)

![partial screenshoot showing blue text in a terminal](assets/images/blue.png)

![partial screenshoot showing red text in a terminal](assets/images/red.png)

3. Validation
Various validation on user input allows the user to run the program without errors. Validation aims to capture various incorrect entries by the user and give feedback to the user. This way the user can give correct input and the program will give the user result. This also prevents the program from crushing. An example of an error validation message can be found below:

![partial screenshot showing error message in a terminal](assets/images/error-message.png)


4. Terminal of 80 characters wide and 24 rows high

## Styling

Styling in the terminal is very limited. The interaction with the user is by Validation errors or messages informing that input has passed validation.
To make the terminal messages more intuitive Colorama colors were introduced. The error messages are in red and positive validation messages are in green. Also, some images were added as welcome and goodbye screens.

If the user wishes to see their booking, it is displayed one line under another so it is clear to see the pairs key-value (date - booking)

## Bugs
1. Issue with accessing data needed to update both worksheets.

    Each set of data: dates, email, room number were local variables in the new booking function. Managed to pass various variables to the functions so each value is read correctly.

2. Issue with Rooms Worksheet

    Recording new booking - new booking was not appearing in the appropriate column for the room. Found that data is saved under identical column numbers as it is saved in the clients worksheet. Found function that was referring to clients worksheet and replaced it with variable worksheet. The worksheet variable had the appropriate worksheet passed to it when the function was called and the correct column in the rooms worksheet was updated.

3. Issue with lenght of the line:

    - the errors were raised in the lines where the if statement was very long. followed advice from [stack overflow](https://stackoverflow.com/questions/5253348/very-long-if-statement-in-python)

    - the error with very long regex - Initially I was reluctant to touch it due to the complexity of the code and worry that I would break it. My mentor Felipe Sousa has suggested a solution on [stack overflow](https://stackoverflow.com/questions/8006551/how-to-split-long-regular-expression-rules-to-multiple-lines-in-python/8006576#8006576) which didn't seem to work fully. I implemented some kind of different solution that didn't break the regex. 

4. The Bug caused by is_empty_cell function.

    The function was supposed to test if the cell is empty, I tried to use it both for validation of new booking as well as cancellation of the existing booking. The logic was incorrect and I created the separate function to is_full_cell - to test if all cells are full. 

5. Bug in deleting the booking from the spreadsheet. 

    - the user inputs the dates for cancelation. The dates are validated for format
    - next the program checks what was the room name on the first date within the cancelation period in the clients spreadsheet
    - the program deletes the booking from the rooms spreadsheet on the basis of what room was within the first day of booking
    - the assumption is that the client will book a longer period of time in the same room, he will not change rooms
    - I tried to capture the room name from the clients spreadsheet, which introduced a new bug, which I have not been managed to fix,
    - I reversed to the version of the function that assumes that the room that is being canceled is the same for the whole cancelation period

    solution: ask the user to input the room which he wants to cancel. Validation needs to match dates and the room.
    return an error if any of the cells are empty within given dates in column room or in column email

6. Double booking

    The program only checks if the room is available on those dates, it can override the entries of old booking under the client's email and add a new booking in a different room. The client would end up having 2 rooms booked at the same time, but only the most recent room would display 

7. Double emails

    The program was allowing to add a new email to the spreadsheet if the user used lower case or upper case differently to the previous entry. Fixed error by returning the email string as all lowercase.

8. Errors inputed by image of the castle

    the gitpod displays various errors, not accepting the characters that are used in the castle image. I need to leave those as they are as it would ruin the image if I delete or edit those characters

9. Error in room number

    When user was putting the letters instead of a number, the validation error was not displaying a correct message. The message was "invalid literal for int() with base 10". This would not help user to estimate what he has done wrong. 

    I added another validation - a regex to validate input if it is numbers or other symbols. I also moved int() function to the elif statement so the input is changed to an integer only after it passes validation that it is actually the number.  The regex I found on [stack overflow](https://stackoverflow.com/questions/50177113/regex-for-only-numbers-in-string) accepts digits and space - which gives the user a little more flexibility if accidental white space is input. 

10. Program crushing when attempting to print dates, when booking was none

    It seems that when the cell value was empty, the python was returning None, not an empty string. Python was returning the error that it can only concat strings, not none.
    I have added if statement to check if the value is an empty string or if the value is none so it converts the val to string "None" This way I could concat string and print the data for the user in the form that I have designed.

11. Gspread error - Exceeded read requests per minute per user.

    During intense testing, I have received the error that I have exceeded the Read requests per minute per user. This seems to be a limitation of the use of a free and simple database like this. The error message can be found [here](assets/images/error-gspread.png).

12. User can't cancel the booking

    One of the testers (something@aol.com) reported that they can see their booking displayed by their program (booking Glasgow  10-20 October 2021), but the program doesn't allow them to cancel this booking. 

    When checking the spreadsheet I realized that this booking was saved in clients_worksheet, but not in rooms_worksheet. Further investigation revealed that the tester had API error during the booking of this room. This interrupted the process of saving data. 

13. Confusing message about the date in the past

    Tester pointed out that the program shows error - Date in the past for today date. This is due Python converting user input from string to Python date-time object, which makes it Today midnight, while python today object takes the time from now. This means that user inputting today's date is considered by python as being in the past.

    I have reworded the error message so it explains that booking is available from tomorrow onwards.  

## Remaining Bugs

From the above mentioned list the bugs that were remaining

8. issue with linting errors raised by image of the castle - I left it untouched as editing it might destroy the image

11. Gspread error - Exceeded read requests per minute per user.

    Gspread seems to be very simple database and sufficient for a small project (or a small hotel). For any robust and reliable website, different type of database should be used. 

12. User can't cancel the booking
    In rare circumstances, the user might not be able to cancel the booking. The database was designed as two worksheets and if anything breaks in between them then the booking is not valid. Unfortunately, it is too late to change the database completely but it is another weakness of the chosen type of database and the formating style of storing data.

## linting
control over errors raised by flake8

control over pylint error messages. File generated automatically by pylint using command:
'''
pylint --generate-rcfile > pylintrc
'''
and modified to ignore some messages. 

## Validation of the user input
Validation has been created in validation file. BaseValidator class has a few methods that allow basic validation
- regex
- validate if member of a list
- validate if not member of a list
- if input not empty

Other validators inherit from Base Validator and extend some of the methods:

1. Email validation
    - used regex to validate if the user's input resembles a standard email
    - program converts the email to small letters and saves it in this format in the spreadsheet to prevent double entries in different formats

2. Date validation
    - used regex to validate the date format
    - checking if the input date is not in the past

3. Period of booking validation
    program checks if the booking is not 
    - shorter than Minimum value of days
    - longer than Maximum value of days
    - the maximum and minimum stay are set as a global variable in validation file
    - end date was input before the start date
4. Room number validation
    - validates if user input is a digit or digit and a white space
    - validates if the number is between 1 - 9

8. User options validation
    - empty input returns value error
    - random letters return an error
    - random words return an error
    - validation looks for keywords to be present

## Testings
I wrote tests for testing user input and testing validation. I used pytest. 

## Deployment

The site was initially deployed to Heroku. For deployment to heroku, please follow below steps.

In light of Heroku removing free tiers, the project was moved to render.

Steps to deploy to render [here](https://code-institute-students.github.io/deployment-docs/10-pp3/)

### Deployment steps (Heroku)

1. add the list of requirements by writing in the terminal "pip3 freeze > requirements.txt"
2. Add six and colorama==0.4.4 as they didn't seem to add automatically
2. Git add and git commit the changes made
3. Log into [Heroku](https://dashboard.heroku.com/apps) or create a new account and log in

4. top right-hand corner click "New" and choose the option Create new app, if you are a new user, the "Create new app" button will appear in the middle of the screen
5. Write app name - it has to be unique, it cannot be the same as this app
6. Choose Region - I am in Europe
7. Click "Create App"

The page of your project opens.
8. Choose "settings" from the menu on the top of the page
9. Go to section "Config Vars" and click button "Reveal Config Vars"

10. Go to git pod and copy the content of "creds.json" file
11. In the field for "KEY" enter "CREDS" - all capital letters
12. Paste the content of "creds.json" and paste to field "VALUE" Click button "Add"
13. Add another key "PORT" and value "8000"

14. Go to section "Build packs" and click "Add build pack"
    - in this new window - click Python and "Save changes"
    - click "Add build pack" again
    - in this new window - click Node.js and "Save changes"
    - take care to have those apps in this order: Python first, Node.js second, drag and drop if needed

15. Next go to "Deploy" in the menu bar on the top 
16. Go to section "deployment method", choose "GitHub"
17. New section will appear "Connect to GitHub" - Search for the repository to connect to
18. type the name of your repository and click "search"
19. once Heroku finds your repository - click "connect"

20. Scroll down to the section "Automatic Deploys"
21. Click "Enable automatic deploys" or choose "Deploy branch" and manually deploy
22. Click "Deploy branch"

Once the program runs:
you should see the message "the app was sussesfully deployed"
23. Click the button "View"


### Deployment steps (Render)
These steps are describing moving the existing project from Heroku to Render.

1. Create account on [render](https://render.com/) or log in
2. click "Create" top right hand corder and choose option "Web service"
3. choose repository from list displayed below. If repository is not listed use "configure account" and link repositories to your render account.
4. Once created - new project will show on "Dashboard" from where it can be managed
5. Go to Dashboard and click into your project. On the left you should see various options - go to "Enviroment"
6. Add following enviromental variables:

| Key | Value|
|---|---|
|  PORT | 8000 |
| PYTHON_VERSION | 3.8.11 |

7. Secret Files - add file name creds.json and add content of the creds file in json format as below example. This file is needed for google api
```
{
  "type": "",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```

### Forking the GitHub repository
By forking out of this repository you will be able to view and edit the code without affecting the original repository. 

1. Locate the GitHub repository. Link can be found [here](https://github.com/JoGorska/hotel-booking).
2. Click the button in the top right-hand corner "Fork"
3. This will take you to your own repository to a fork that is called the same as the original branch. 

### Making a local clone

1. Locate the GitHub repository. Link can be found [here](https://github.com/JoGorska/hotel-booking).
2. Next to the green Gitpod button you will see a button "code" with an arrow pointing down
3. You are given the option to open with GitHub desktop or download zip
4. You can also copy https full link, go to git bash and write git clone and paste the full link


## Further developement the website

1. Change excel spreadsheet to a real database

    The system of saving data that I have introduced inputs a new column each time a new user is registered. This makes the spreadsheet really big.
    I have prepared the spreadsheet to accommodate booking until 26/05/2024. Any further booking would require manually extending the spreadsheet to add more rows and more dates. 
    Each booking should be registered as a new row with email, date, room as the columns and have a unique reference number. This way the user would be able to easily refer to this particular booking, cancel it or change it.

    Gspread has also strong limitations on a number of API requests. It was not good for the testing of the app. I can also see the problems if the hotel was introducing any last-minute deals - the database would get blocked with too many clients trying to book at the same time.

2. Connect to the live page of the hotel
    In this day and age it is not realistic to ask user to book a room in a hotel in something that resambles commandline interface. Having that said - this concept of hotel bookin and validating dates and rooms availibility will be explored further. My previous project Cath's cats Castle can be found [here](https://jogorska.github.io/Luxury_cat_hotel/index.html) is a front end application and does not allow users to register and book a room. This page will need a back end connected to it. Some logic build in this application could be reviewed and used in upgrade of this application"


## User stories

### First time visitor

- I want to be able to add a booking
- I want to be able to check if the room is available for me to book
- Once I added my booking I want to be able to change it or cancel.
- I want to be able to print my booking.
- I want to be able to quit the program and not continue with the booking.

### The goals were accomplished in the following ways

- First time visitor is given the option to add booking.
- First-time visitor can use the option to show the room's availability. The user can choose dates and a room, that he wants to check. 
- Once his new booking is saved, he is given options to change it or cancel
- After the booking is completed the user can print his booking to the terminal
- User can quit the program as soon as the options are shown. This can be after he has input his email or after completed the booking

### Returning visitor

- I would like the program to recognize my email as a returning customer.
- I want to be able to add a new booking.
- I want to be able to change my booking.
- I want to be able to cancel my booking.
- I would like to be able to check if the room is available on my chosen dates
- I would like to check my booking.

### The goals were accomplished in the following ways

- Program checks the user's email and displays a welcome message when the email is found in the database.
- The option to show room's availability is enabled for returning customer as well. User can choose dates and room, that we wants to check. 
- Once his new booking is saved, he is given options to change it or cancel
- After the booking is completed the user can print his own booking to the terminal
- User can quit the program as soon as the options are shown. This can be after he has input his email or after completed booking


## Technologies used
- Code Institute template with HTML and CSS
- Python
- google sheets
- Libraries:
    * gsptread
    * re
    * colorama
    * google.oauth2.service_account
    * datetime


## Code Validation

1. [Pep8online](http://pep8online.com/)


The code has been put through validation Pep8online. I have checked the errors displayed initially. The error reports can be found here: [first report](assets/images/pep8-errors.png), [third reprot from pep8](assets/images/pep8-third.png). The final version of the report can be found below:

Line 333, 598. 944, 945, 992 - if statement is very long in those lines and had to be split into two lines. Pip8 returns it as an error, alternative would be to have the whole if statement in one line - then pip8 would return the error - line too long. 

## Manual testing
![final report](assets/images/pep8-final.png)

1. Different operating system
    * Windows computer: all working correctly
    * Linux computer: all working correctly
    * Samsung galaxy note 8: all working correctly
    * Samsung galaxy A40: instead of the input that the user is trying to type it inputs random letters or numbers. The screenshot option is blocked on this phone (work phone) The photo of the screen can be seen [here](assets/images/samsunga40.png). It seems like it is an issue of the phone, rather than an app. It might be something to do with autofill.

2. Testing user input validation
    * email
        - submitting empty input returns an error
        - missing "@" - returns error
        - full stop "." in the wrong place - returns an error
        - putting letters only returns an error
        - putting numbers only returns an error

    * dates
        - submitting an empty field returns an error
        - putting all numbers returns an error
        - putting all letters returns an error
        - putting date with "." instead of "/" returns an error
        - putting month one digit only returns an error
        - putting year as two-digit only returns an error
        - putting the date in the past returns an error
        - putting end date earlier than starts date returns error after the period of booking is validated
    * room
        - putting letters instead of numbers returns validation error that you have entered other characters than a number
        - putting other characters - not numbers returns the same validation error
        - program returns a validation error when two-digit number is entered instead of one digit
        - empty input gives an error that you have entered other characters than a number.

    * returning user options
        - putting empty value returns validation error
        - putting numbers, random letters or signs returns a validation error

3. Gramarly

Used [gramarly](https://app.grammarly.com) for spell check for README.md and run.py


## Thanks to
- [Code Institute Template](https://github.com/Code-Institute-Org/python-essentials-template)
- [Asciiart](https://www.asciiart.eu/buildings-and-places/castles)
- Fernanda Brito - for help with Readme 
- Richard Eldridge - for extensive testing
- Felipe Sousa Alarcon - for mentoring 
