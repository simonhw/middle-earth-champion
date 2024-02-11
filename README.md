# Scout Group Waiting List

![GitHub last commit](https://img.shields.io/github/last-commit/simonhw/waiting-list)

## Contents
- [User Experience](#user-experience)
    - [Initial Discussion](#initial-discussion)
    - [User Stories](#user-stories)
- [Design](#design)
    - [Lucidchart Flowchart](#lucidchart-flowchart)
- [Features](#features)
- [Dependencies](#depenencies)
- [Bugs](#bugs)
    - [Known Bugs](#known-bugs)
    - [Solved Bugs](#solved-bugs)


## User Experience
### Initial Discussion
This application is designed to be run in a terminal environment. Its purpose is to take in user information and add it to a database for a club membership waiting list. The application can also be used to check if their position on the waiting list has changed.

### User Stories
#### First-time Visitor Goals
- To understand the purpose of the program.
- To enter data without error or confusion.

#### Returning Visitor Goals
- To edit incorrect data in their entry
- To check their data and position in list

#### Frequent Visitor Goals
- To edit and amend entries on the list

## Design
### Lucidchart Flowchart

![Lucidchart flowchart version 1](assets/images/readme/flowchart_v1.png)

## Features
- Take in user details: name, phone number, child's name, date of birth
- confirm user data
- return waitiing list reference number
- return which age section the child will be joining
- allow user to check their position using the ref number

## Depenencies
[Colorama](https://pypi.org/project/colorama/)

## Bugs
### Known Bugs

### Solved Bugs
| # | Bug | Image | Solution |
| --- | --- | --- | --- |
| 1 | Validating user choice crashed the code passing a letter into int(). | | Set choice check to '1' '2' '3' to avoid this. |
| 2 | dob had time at the end in 0s. || Adding .date() to the end removed them. |

## To-do List
- Update validate_name function to allow hyphens and spaces
- Add email validation