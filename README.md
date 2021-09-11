# Cath's Cats' Castle - booking
## Screenshot 

![showpiece start screen](assets/images/showpiece.png)


link to live page [here](https://caths-cats-castle-booking.herokuapp.com/)



## Aim of the program

The aim of the website is to allow users to book their cats' stay in the hotel. 

## Structure of the program

The program is a comand line program that leads the user through series of questions. 
1. Start
The user is asked for the email
2. The program checks if it is a returning customer

## Features

1. Image - [ascii art](https://www.asciiart.eu/buildings-and-places/castles)
the image of the castle is shown when the program starts. This gives a nice introduction to the product.

2. [Colorama](https://pypi.org/project/colorama/)
added feature to allow different colors of fonts to display in the terminal. The aim of this feature is to help the user understand what the program is doing or what is expected of the user. Since comand line interface is not user friendly, the user is not used to read various lines to understand that there was error returned. Once the error message is in red it stands out amongs other lines and allow user to action on it. 

While the program is saving things in the spreadsheet it can take a while. The blue lines of code informing the user that the program is saving data help the user to understand that the program is still working, it hasn't broken, it is just taking the time to save data.
- the ValidationErrors are displaid in red
- the positive validation messages are displayed in green
- the information about saving data in spreadsheet are displayed blue

3. Validation
Various validation on user input allows the user to run the program without errors. The aim of validation is to capture varius incorrect entries by the user and give feedback to the user. This way the user can give correct input and the program will give the user result. 

4. Terminal of 80 characters wide and 24 rows high

## Styling


## Bugs
1. Issue with accessing data needed to update both worksheets. Each set of data: dates, email, room number were local variables in the new booking function. Managed to pass various variables to the functions so each value is read correctly.

2. Issue with Rooms Worksheet - recording new booking - new booking was not apearing in the apropriate column for the room. Found that data is saved under identical column number as it is saved in clients worksheet. Found function that was refering to clients worksheet and replaced it with variable worksheet. Worksheet wariable had the appropriate worksheet passed to it when the function was called and the correct column in the rooms worksheet was updated.

3. Issue with lenght of the line:
- the errors were raised in the lines where the if statement was very long. followed advice from [stack overflow](https://stackoverflow.com/questions/5253348/very-long-if-statement-in-python)
- the error with very long regex - I left it untouched as I am concerned that it would stop working

4. Bug caused by is_empty_cell function. The function was supposed to test if the cell is empty, I tried to use it both for validation of new booking as well as cancellation of the existing booking. There logic was incorrect and I created the seperate function to is_full_cell - to test if all cells are full. 

5. Bug in deleting the booking from the spreadsheet. 
    - the user inputs the dates for cancelation. The dates are validated for format
    - next the program checks what was the room name on the first date within cancelation period in the clients spreadsheet
    - the program deletes the booking from the rooms spreadsheet on the basis of what room was within the first day of booking
    - the assumption is that the client will book a longer period of time in the same room, he will not change rooms
    - I tried to capture the room name from the clients spreadsheet, which introduced a new bug, which I have not been managed to fix,
    - I reversed to the version of the function that assumes that the room that is being cancelled is the same for the whole cancelation period
    solution: ask the user to input the room which he wants to cancel. Validation needs to match dates and the room.
    return an error if any of the cells are empty within given dates in column room or in column email
6. Double booking
Program only checks if the room is available on those dates, it can over ride the entries of old booking under the client's email and add an new booking in a different room. The client would end up having 2 rooms booked in the same time, but only the most recent room would display under his name.

7. Double emails
Program was allowing to add a new email to spreadsheet if the user used lower case or upper case differently to previous entry. Fixed error by returning the email string as all lowercase.

8. Errors inputed by adding the image of the castle
the gitpod displays various errors, not accepting the characters that are used in the castle image. I need to leave those as they are as it would ruin the image if I delete or edit those characters


## Remaining Bugs
From the above mentioned list the bugs that were remaining
3. issue with very long regex. I do not want to break this complex code. I left it untouched
8. issue with errors raised by image of the castle - I left it untouched as editing it might destroy the image
  
## Validation

1. Email validation
- used regex to validate if the user's input resambles a standard email
- program converts the email to small leters and save it in this format in the spreadsheet to prevent double entries in different formats

2. Date validation
- used regex to validate the date format
- checking if the input date is not in the past

3. Period of booking validation
program checks if the booking is not 
- shorter than 7 days
- longer than 30 days
- end date was input before start date

## Deployment

1. add list of requirements by writing in the terminal "pip3 freeze > requirements.txt"
2. Add six and colorama==0.4.4 as they didn't seem to add automaticaly
2. Git add and git commit the changes made
3. Log into [Heroku](https://dashboard.heroku.com/apps) or create new account and log in

4. top right hand corner click "New" and choose option Create new app, if you are new user, the "Create new app" button will apear in the middle of the screen
5. Write app name - it has to be unique, it cannot be the same as this app
6. Choose Region - I am in Europe
7. Click "Create App"

The page of your project opens.
8. Choose "settings" from the menu on the top of the page
9. Go to section "Config Vars" and click button "Reveal Config Vars"

10. Go to git pod and copy the content of "creds.json" file
11. In the field for "KEY" enter "CREDS" - all capital letters
12. Paste content of "creds.json" and paste to field "VALUE" Click button "Add"
13. Add another key "PORT" and value "8000"

14. Go to section "Build packs" and click "Add build pack"
    - in this new window - click Python and "Save changes"
    - click "Add build pack" again
    - in this new window - click Node.js and "Save changes"
    - take care to have those apps in this order: Python first, Node.js second, drag and drop if needed

15. Next go to "Deploy" in menu bar on the top 
16. Go to section "deployment method", choose "github"
17. New section will apear "Connect to github" - Search for repository to connect to
18. type the name of your repository and click "search"
19. once heroku finds your repository - click "connect"

20. Scroll down to section "Automatic Deploys"
21. click "Enable automatic deploys" or choose "Deploy branch" and manualy deploy
22. Click "Deploy branch"

Once the program runs:
you should see the message "the app was sussesfuly deployed"
23. Click button "View"



## Further developement the website

Next important feature that needs to be developed is the "print" option
- to display user's booking
- to display available dates in particular room

## User stories



## Technologies used
python

## Testing

1. [Pep8online](http://pep8online.com/)
![errors report](assets/images/pep8-errors.png)

I have checked the errors displayed initialy by pep8online. I have tried to correct those errors.

![second errors report](assets/images/pep8-final.png)

- line 319 - error line too long is caused by Regex. I do not feel competent enough to split this regex into lines without damaging it's functionality
- line 304, 553, 717 - if statement is very long in those lines and had to be split into two lines. Pip8 returns it as an errror, alternative would be to have whole if statement in one line - than pip8 would return error - line too long. 

2. Windows computer:

3. Linux computer:

4. Samsung galaxy note 8

5. samsung????
user tries to click on letters on the phone's keyboard, but in the program it displays as varous random letters. 

## Thanks to
- [Asciiart] (https://www.asciiart.eu/buildings-and-places/castles)


