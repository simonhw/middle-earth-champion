# Scout Group Waiting List

Deployed program on Heroku: [Scout Group Waiting List](https://scouts-waiting-list-7d813d9f1b2e.herokuapp.com/)

![GitHub last commit](https://img.shields.io/github/last-commit/simonhw/waiting-list)

## Contents
- [User Experience](#user-experience)
    - [Initial Discussion](#initial-discussion)
    - [User Stories](#user-stories)
- [Design](#design)
    - [Lucidchart Flowchart](#lucidchart-flowchart)
    - [Colours](#colours)
- [Features](#features)
- [Dependencies](#dependencies)
- [Bugs](#bugs)
    - [Known Bugs](#known-bugs)
    - [Solved Bugs](#solved-bugs)


## User Experience
### Initial Discussion
This application is designed to be run in a terminal environment. Its purpose is to take in user information and add it to a database for a club membership waiting list. Users may also use the application to check their child's position on the waiting list. Admin users are able to view the content of the waiting list and delete entries where appropriate.

### User Stories
#### First-time Visitor Goals
- To understand the purpose of the program.
- To enter data without error or confusion.
- To ensure data is correct before submission.

#### Returning Visitor Goals
- To check their child's position in the waiting list.

#### Frequent Visitor Goals
- To view and delete entries on the list.

## Design
### Lucidchart Flowchart
An inital concept was developed in a flowchart to give a good sense of the flow of the program and how the users would interact with inputs.

![Lucidchart flowchart version 1](assets/images/readme/flowchart_v2.png)

### Colours
The Colorama module was utilised to introduce some colour to the program. Headings were given a blue foreground colour reflective of the Scout uniform in Ireland. Error warning messages were given a red colour to bring attention to the user that something has gone wrong. 

In admin mode, each age section has an associated foreground colour related to the section badge: red for Beavers; green for Cubs; blue for Scouts, since there is no orange option and yellow was not pleasing to the eye; and magenta for Ventures, being the closest available colour to purple. The colours are also used for the headings when each waiting list is displayed for the admin user.

![Beaver section badge](assets/images/readme/beaver-badge.png)
![Cub section badge](assets/images/readme/cub-badge.png)
![Scout section badge](assets/images/readme/scout-badge.png)
![Venture section badge](assets/images/readme/venture-badge.png)

## Features
This program is written completely in Python. The inital scope of the project was set out to achieve the following:
- Take in user details: name, phone number, contact email, child's name, and child's date of birth
- Confirm the user data
- Return a waitiing list reference number
- Return which age section the child will be joining
- Allow user to check their position using the reference number
- Allow an admin to view the waiting lists and delete rows

All of these goals were achieved in this version of the program.

The user is greeted on running the program by a descriptive header welcoming them to the waiting list of the 101st Dublin Scout Group. This is a fictional group (currently not on the list of active scout groups).

Clear instructions are given to the user explaining what to do next to use the program. Only four inputs are accepted: The numbers `1`, `2`, `3`, or `4`.

![Welcome menu](assets/images/readme/welcome-menu.png)

### Option 1
If the user enters `1`, feedback is given via a descriptive heading to confirm that the program is ready to add their child to the waiting list.

![Option 1 heading](assets/images/readme/option-1-name.png)

The user is then prompted to enter their first name, last name, contact email, child's first name, child's last name, and child's date of birth. The details are printed to the terminal and the user is asked to confirm them. If they enter `n`, the previous prompts repeat.

![Entering details](assets/images/readme/enter-details.png)
![Confirming details](assets/images/readme/confirm-details.png)

If the user enters `y`, the data is sent to the Google Sheets spreadsheet and a confirmation message is shown if successful. This message confirms which age section the child will join and the reference number that the user needs to use to check their position in the list.

![Details successfully pushed](assets/images/readme/details-pushed.png)

The user is given the option to return to the main menu by inputting `y` or exit the program with `n`.

### Option 2
If the user selects option `2`, another descriptive heading is shown.

![Option 2](assets/images/readme/option-2.png)

When the user enters a reference code, a message is printed to inform them that it is being verified. If valid, their child's position in the waiting list is printed to the terminal along with the name of the age section.

![Successful reference code check screen]()

The user is again given the option to return to the main menu by inputting `y` or exit the program with `n`.

### Option 3
If an admin user wants to view and edit the waiting list, they can enter `3`. A password request is presented to prevent unauthorized access to the data.

![Admin log in screen]()

Upon successful login, the admin user is presented with a list of the waiting lists to choose from. Entering a number from `1` to `4` prints the respective waiting list to the terminal in the form of lists of the data entries.

![Section choice screen]()

The chosen waiting lists is printed under a descriptive heading.

![Beaver waiting list screen]()

At this point the admin user is given the option to delete someone from the waiting list for any reason e.g. the child has been enrolled or changed their mind about joining.

Entering `y` will present a new input asking the user to select a number from the list corresponding to the data row they wish to delete. When a number is chosen, the input choice is shown on screen as well as details of the data row being deleted. 
Messages then print to say an attempt is being made to delete the row and if the row was successfully deleted.

![Data deleted successfully screen]()

An option to delete another entry is presented to the user. If `y` is entered, the updated waiting list in printed to the terminal again and the same steps above are follows. If `n` is entered, the user is asked if they want to view the waiting lists again and the same processes follow as above.

![Edit another section screen]()

Finally, the user is given the option to return to the main menu by inputting `y` or exit the program with `n`.

### Option 4
To exit the program, the user can `4`. Before full shutdown, a message prints to let them know the program is closing.

![Exit program screen]()

## Validation
All user inputs and gspread processes are validated by the program. Each validation check is explained below and fully comprehensive testing of the validation is detailed in the [Manual Testing section](#manual-testing).

### Validating Names
The user inputs for the parent's first name, parent's last name, child's first name, and child's last name are subjected to a name validation check.

The `validate_name()` function takes in two strings as parameters: the message to be printed, and a description of the name being validated. The function asks for input and removes any leading and trailing whitespaces with `.strip()`. The string is then searched for any numbers and a ValueError is raised if they are found.

![Validate name number error gif]()

If the string contains at least two characters, the input is returned with the first letter capitalised using `.title()`, otherwise a Value Error is raised.

![Validate name 1 character error gif]()

### Validating Emails
The `validate_email()` function uses RegEx to check if the user input matches the specified email format:

- Name made up of any word or hypen or full stop: `[\w\.-]` e.g. `john.smith`
- The `@` symbol
- A domain name made up of any word including hyphens: `[\w-]` e.g. `foresty-group`
- A full stop `.`
- The rest of the domain made up of any words and full stops: `[\w\.]` e.g. `.co.uk`

Put together, the RegEx pattern for this is 
`^[\w\.-]+@[\w-]+\.+[\w\.]+$`

![Email pattern test on RegEx](assets/images/readme/email-test.png)

If the user enters an invalid input, the below error is shown which reminds the user of the correct email format required.

![Invalid email error message]()

Valid inputs are returned by the funtion.

### Validating Dates of Birth
The `validate_dob()` fuction asks the user to input their child's date of birth in the format `DD/MM/YYYY`. 

## Dependencies
- [Colorama](https://pypi.org/project/colorama/)
- [Gspread]()
- [Google Auth]()
- [Datetime]()
- [Math]()
- [Random]()
- [Re]()

## Bugs
### Known Bugs

### Solved Bugs
| # | Bug | Image | Solution |
| --- | --- | --- | --- |
| 1 | Validating user choice crashed the code passing a letter into int(). | | Set choice check to '1' '2' '3' to avoid this. |
| 2 | dob had time at the end in 0s. || Adding .date() to the end removed them. |
| 3 | When refactoring `get_details()` the error message printed once for each spreadsheet searched instead of just printing once and requesting new user input. | ![Get details error messages](assets/images/readme/bugs/bug-ref-loops.png) | The else was changed to an if statement and indented back to the level of the while loop. |
| 4 | When entering an email with more than one `.` in the domain name, the input was rejected. | ![Email domain error](assets/images/readme/bugs/email-bug.png) | |
| 5 | After deleting a row from the waiting list, the code as it was did not update the numbers associated with the remaining entries and the user could delete the wrong entry or keep deleting the last entry which would be a blank row. | | |

## Credits
The images of the badges in this README were taken from the Scout Shop [website](https://thescoutshop.ie/collections/badges).

## To-do List
- Update validate_name function to only allow one space and/or one hypen between letters
- hash the admin password
- allow user to return to main menu from any input line
- add code to show a maximum number of rows at a time if the waiting list is very long?
- fix waiting list delete loop 