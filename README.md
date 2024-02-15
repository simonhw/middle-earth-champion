# Scout Group Waiting List

Deployed program on Heroku: [Scout Group Waiting List]()

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

The user is greeted on running the program by a descriptive header.

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

## Credits
The images of the badges in this README were taken from the Scout Shop [website](https://thescoutshop.ie/collections/badges).

## To-do List
- Update validate_name function to only allow one space and/or one hypen between letters
- hash the admin password
- allow user to return to main menu from any input line
- add code to show a maximum number of rows at a time if the waiting list is very long?