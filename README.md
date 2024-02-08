# Title Pending

(Waiting List Idea)
This application is designed to be run in a terminal environment. Its purpose is to take in user information and add it to a database for a club membership waiting list. The application can also be used to check if their position on the waiting list has changed.

Features
- Take in user details: name, phone number, child's name, date of birth
- confirm user data
- return waitiing list reference number
- return which age section the child will be joining
- allow user to check their position using the ref number

## Lucidchart Flowchart

![Lucidchart flowchart version 1](assets/images/readme/flowchart_v1.png)

## Depenencies
[Colorama](https://pypi.org/project/colorama/)

## Bugs
Validating user choice crashed the code passing a letter into int(). 
Set choice check to '1' '2' '3' to avoid this.