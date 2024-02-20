# Scout Group Waiting List

Deployed program on Heroku: [Scout Group Waiting List](https://scouts-waiting-list-7d813d9f1b2e.herokuapp.com/)

![GitHub last commit](https://img.shields.io/github/last-commit/simonhw/waiting-list)
![GitHub contributors](https://img.shields.io/github/contributors/simonhw/waiting-list)

## Contents
- [User Experience](#user-experience)
    - [Initial Discussion](#initial-discussion)
    - [User Stories](#user-stories)
- [Design](#design)
    - [Lucidchart Flowchart](#lucidchart-flowchart)
    - [Colours](#colours)
- [Features](#features)
    - [Option 1 - Registering Details](#option-1---registering-details)
    - [Option 2 - Checking Position on Waiting List](#option-2---checking-position-on-waiting-list)
    - [Option 3 - Viewing and Editing the Waiting Lists](#option-3---viewing-and-editing-the-waiting-lists)
    - [Option 4 - Exiting the Program](#option-4---exiting-the-program)
    - [Features to be Implemented](#features-to-be-implemented)
- [Technologies Used](#technologies-used)
    - [Languages](#languages)
    - [Frameworks, Libraries, and Programs](#frameworks-libraries-and-programs)
    - [Dependencies](#dependencies)
- [Deployment](#deployment)
    - [Local Deployment](#local-deployment)
    - [Live Deployment](#live-deployment)
- [Testing](#testing)
- [Credits](#credits)
    - [Media](#media)
    - [Code Used](#code-used)
- [Acknowledgements](#acknowledgements)


## User Experience
### Initial Discussion
This application is designed to be run in a terminal environment. Its purpose is to take in user information and add it to a database for a club membership waiting list. Users may also use the application to check their child's position on the waiting list. Admin users can view the content of the waiting list and delete entries where appropriate.

### User Stories
#### First-time Visitor Goals
- To understand the purpose of the program.
- To enter data without error or confusion.
- To ensure data is correct before submission.

#### Returning Visitor Goals
- To check their child's position on a waiting list.

#### Frequent Visitor Goals
- To view and delete entries on a waiting list.

## Design
### Lucidchart Flowchart
An initial concept was developed in a flowchart to give a good sense of the flow of the program and how the users would interact with inputs.

![Lucidchart flowchart version 1](assets/images/readme/flowchart_v2.png)

### Colours
The Colorama module was utilised to introduce some colour to the program. Headings were given a blue foreground colour reflective of the Scout uniform in Ireland. Error warning messages were given a red colour to bring attention to the user that something has gone wrong. 

In admin mode, each age section has an associated foreground colour related to the section badge: red for Beavers; green for Cubs; blue for Scouts, since there is no orange option and yellow was not pleasing to the eye; and magenta for Ventures, being the closest available colour to purple. The colours are also used for the headings when each waiting list is displayed for the admin user.

![Beaver section badge](assets/images/readme/beaver-badge.png)
![Cub section badge](assets/images/readme/cub-badge.png)
![Scout section badge](assets/images/readme/scout-badge.png)
![Venture section badge](assets/images/readme/venture-badge.png)

## Features
This program is written completely in Python. The initial scope of the project was set out to achieve the following:
- Take in user details: name, phone number, contact email, child's name, and child's date of birth
- Confirm the user data
- Return a waiting list reference number
- Return which age section the child will be joining
- Allow user to check their position using the reference number
- Allow an admin to view the waiting lists and delete rows

All of these goals were achieved in this version of the program.

When the program launche, the user is greeted by a descriptive header welcoming them to the waiting list of the 101st Dublin Scout Group. This is a fictional group (currently not on the list of active scout groups).

Clear instructions are given to the user explaining what to do next to use the program. Only four inputs are accepted: The numbers `1`, `2`, `3`, or `4`.

![Welcome menu](assets/images/readme/welcome-menu.png)

### Option 1 - Registering Details
If the user enters `1`, feedback is given via a descriptive heading to confirm that the program is ready to add their child to the waiting list.

![Option 1 heading](assets/images/readme/option-1-name.png)

The user is then prompted to enter their first name, last name, contact email, child's first name, child's last name, and child's date of birth. The details are printed to the terminal and the user is asked to confirm them. If they enter `n`, the previous prompts repeat.

![Entering details](assets/images/readme/enter-details.png)
![Confirming details](assets/images/readme/confirm-details.png)

If the user enters `y`, a unique reference number is generated and two Class instances take in the user inputs and return a list of the values. This could also be achieved by simply appending the inputs to a list one by one but using the Classes makes the code look more elegant and tidy, and also provides evidence of my understanding of Python Classes. The lists are concatenated and sent to the Google Sheets spreadsheet. A confirmation message is shown if this process succeeds. This message also confirms which age section the child will join and the reference number that the user needs to use to check their position in the list.

![Details successfully pushed](assets/images/readme/details-pushed.png)

The user is given the option to return to the main menu by inputting `y` or exit the program with `n`.

#### Cancel Registration of Details
Should the user wish to abort the process of entering details or if they get stuck in a loop entering invalid inputs over and over, they may type `menu` into the terminal and the program will return the user to the main menu.

<summary><details>Gif of user exiting the details registration process early</details>

![Exiting details process early gif]()

</summary>

### Option 2 - Checking Position on Waiting List
If the user enters `2`, another descriptive heading is shown.

![Option 2](assets/images/readme/option-2.png)

When the user enters a reference code, a message is printed to inform them that it is being verified. If valid, their child's position on the waiting list is printed to the terminal along with the name of the age section.

![Successful reference code check screen](assets/images/readme/check-ref-code.png)

The user is again given the option to return to the main menu by inputting `y` or exit the program with `n`.

If the user enters an invalid code three times, they are given the option to exit the process or continue attempting to enter a code. This check repeats for every three invalid attempts.

![Forgot reference code check]()

### Option 3 - Viewing and Editing the Waiting Lists
If an admin user wants to view and edit the waiting list, they can enter `3`. A password request is presented to prevent unauthorized access to the data. If the user enters an invalid password three times, they are given the option to exit the process or continue attempting to enter a password. This check repeats for every three invalid attempts.

![Admin log in screen](assets/images/readme/admin-screen.png)

![Forgot password code check]()

Upon successful login, the admin user is presented with a list of the waiting lists to choose from. Entering a number from `1` to `4` prints the respective waiting list to the terminal in the form of lists of the data entries.

![Section choice screen](assets/images/readme/section-choice-screen.png)

The chosen waiting list is printed under a descriptive heading.

![Beaver waiting list screen](assets/images/readme/beavers-waiting-list.png)

At this point, the admin user is given the option to delete someone from the waiting list for any reason e.g. the child has been enrolled or changed their mind about joining.

Entering `y` will present a new input asking the user to select a number from the list corresponding to the data row they wish to delete. When a number is chosen, the corresponding name of the child to be removed from the waiting list is shown. The user is then asked to confirm the action of deletion. Entering `n` will cancel this process and ask the user if they want to edit another section. Entering `y` will print a message saying an attempt is being made to delete the row and then another message either stating that the row was successfully deleted or that something went wrong accessing the data.

![Data deleted successfully screen](assets/images/readme/successful-delete.png)

An option to delete another entry is presented to the user. If `y` is entered, the updated waiting list is printed to the terminal again and the same steps above are followed. If `n` is entered, the user is asked if they want to view the waiting lists again and the same processes follow as above.

![Edit another section screen](assets/images/readme/edit-another-section.png)

Finally, the user is given the option to return to the main menu by inputting `y` or exit the program with `n`.

#### Large Waiting Lists
A later addition to this program tackled the idea of printing a long waiting list to the terminal. I decided to initially limit the display of large lists to the first 15 data entries only, as this looked neat in the confines of the 24-row high Heroku terminal. The user can choose to then print the rest of the rows if they wish. In each instance, they are then given the option to select a row to delete.

<details><summary>Gif of a large waiting list being viewed</summary>

![Large Waiting List](assets/images/readme/long-waiting-list.gif)

</details>

### Option 4 - Exiting the Program
To exit the program, the user can enter `4`. Before full shutdown, a message prints to let them know the program is closing.

![Exit program screen](assets/images/readme/exit-program-screen.png)

### Features to be Implemented
- Allow a user to edit their existing details using their reference code.

## Technologies Used
### Languages
Python

### Frameworks, Libraries, and Programs
[Lucidchart](https://lucid.app/) - To create flowcharts.

Visual Studio Code and [Gitpod](https://www.gitpod.io/) - The IDEs used to write my code.

[Git](https://git-scm.com/) - For version control.

[GitHub](https://github.com/) - To save and store files online.

[W3Schools.com](https://www.w3schools.com/) and [The Python Library](https://docs.python.org/3/library/) - For researching and learning about Python methods and syntax.

[ScreenToGif](https://www.screentogif.com/) - To create gif files for this README.

Adobe Photoshop 2020 - To pixellate and crop some README images.

[Heroku](https://www.heroku.com/) - To host the deployed version of the program.

[Sheilds.io](https://shields.io/) - To add badges to this README.

[CI Python Linter](https://pep8ci.herokuapp.com/#) - To ensure code meets minimum PEP8 standards.

### Dependencies
- [Colorama](https://pypi.org/project/colorama/) - To apply some colour to text in the program.
- [Gspread](https://docs.gspread.org/) - API allowing manipulation of data with a Google Sheet spreadsheet.
- [Google Auth](https://google-auth.readthedocs.io/) - API to control access to the spreadsheet.
- [Datetime](https://github.com/python/cpython/tree/3.12/Lib/datetime.py) - To work with strings and integers as dates in the code.
- [BCrypt](https://pypi.org/project/bcrypt/) - To hash passwords.
- [Random](https://github.com/python/cpython/tree/3.12/Lib/random.py) - To generate random numbers.
- [Re](https://github.com/python/cpython/tree/3.12/Lib/re/) - To work with regular expression operations.

## Deployment
The program was deployed on Heroku to allow the CI assessor and other interested parties to view and interact with the program.

### Local Deployment
To deploy this program locally on your device, please follow the steps below:

#### Forking
1. Log in or sign up to GitHub.
2. Navigate to the repository for [Scout Waiting List](https://github.com/simonhw/waiting-list).
3. Click the Fork button located in the top right part of the webpage.

#### Cloning
1. Log in or sign up to GitHub.
2. Navigate to the repository for [Scout Waiting List](https://github.com/simonhw/waiting-list).
3. Click on the green Code button, select your preferred option of HTTPS, SSH, or GitHub CLI, and copy the relevant link.
4. Open the terminal in your IDE and navigate to your directory of choice for this new clone.
5. Type `git clone` into the terminal and paste in your copied link. Press enter.

### Live Deployment
#### Setting Up API Credentials
1. Log in or sign up to [Google Cloud Platform](https://console.cloud.google.com/).
2. On your dashboard, click "Create Project".
3. Enter a name for your project and click "Create".
4. Navigate to "APIs & Services" on the left-hand side of the page.
5. Search for the Google Drive API and click "Enable".
6. In the API overview, click "Create Credentials".
7. In the next page, select the following options:
    - "Which API are you using?": Google Drive API
    - "Where will you be calling the API from?": Web Server
    - "What data will you be accessing?": Application data
8. Click "No" for the final question and then click "What credentials do I need?"
9. In this next page, enter a service account name, select the Project/Editor role, and select JSON as the key type.
10. Click continue and wait for the JSON file to download to your computer.
11. Store this file in your local repository and rename it `creds.json`.
12. Navigate back to "APIs & Services" and search for and enable the Google Sheets API.

#### Heroku
1. Log in or sign up to Heroku.
2. On the Heroku dashboard, click "Create New App".
3. Enter a name and select a region then click "Create App".
4. Navigate to the Setting tab and click on "Show Config Vars."
5. Enter `CREDS` into the key field and the `creds.json` file contents into the value field.
6. Enter `PORT` into the next key field and `8000` into the corresponding value field.
7. Below the config vars, click the "Add Buildpack" button.
8. Click Python and "Save Changes".
9. Open the buildpack menu again, click nodejs, and click "Save Changes".
10. At the top of the site, navigate to the "Deploy" tab and select GitHub as the deployment method. Click the "Connect to GitHub" button.
11. Log in to GitHub if and when prompted.
12. Find your repository using the search feature and click "Connect".
13. Scroll down to the Manual Deploy section and click "Deploy Branch".
14. Wait for the compiler to finish and once the message "Your app was successfully deployed." is shown, click "View" to view your program!

## Testing
All documentation on the testing of this application can be found in the [TESTING.md](/TESTING.md) files

## Credits
### Media
The images of the badges in this README were taken from the Scout Shop [website](https://thescoutshop.ie/collections/badges).

### Code Used
**All code in this project was written entirely by Simon Henleywillis unless otherwise specified below.**

The idea to use Gspread and Google Auth was inspired by the Love Sandwiches walkthrough project. Lines 8 to 17 of `run.py` were taken from there as the Google Sheets setup was the same for this project.

Code used to exclude certain symbols from accepted in `validate_name()` was taken from a comment on a Stack Overflow post:
- [Stack Overflow - Validating existence of symbols in input](https://stackoverflow.com/questions/64236875/validating-existence-of-symbols-in-input)

Line 144 uses the method `re.fullmatch`. This was discovered on a Stack Overflow post:
- [Differences between re.match, re.search, re.fullmatch [duplicate]](https://stackoverflow.com/questions/58774029/differences-between-re-match-re-search-re-fullmatch)

Line 210 which converts the user input string date to a true date format was taken from a comment on a Stack Overflow post:
- [Stack Overflow - How do I check date of birth format is correct](https://stackoverflow.com/questions/44716920/how-do-i-check-date-of-birth-format-is-correct)

The line `if __name__ == "__main__":` was included to call my main code functions after discussions with my CI mentor.

The use of bcrypt to hash the admin password was suggested by my CI mentor. This tutorial on [TutorialsPoint.com](https://www.tutorialspoint.com/hashing-passwords-in-python-with-bcrypt) was followed to generate a hashed password. In the process of understanding how to use it effectively, I came across the below post on Stack Overflow that solved issues I had with decoding and encoding the plaintext user input.
- [Stack Overflow - storing and retrieving hashed password in postgres](https://stackoverflow.com/questions/77897298/storing-and-retrieving-hashed-password-in-postgres)

## Acknowledgements
- Thanks to the Code Institute tutors for suggesting Gitpod as a way to get around Known Bug #1 while coding this program.
- Thanks to my CI Mentor [Graeme Taylor](https://github.com/G-Taylor) for his great support and encouragement and especially for showing me that I could use RegEx to validate the email input.
- [Creating Your First README - Kera Cudmore](https://github.com/kera-cudmore/readme-examples)

## To-do List
- add images for all bugs
- final read through of the readme 
- CI linter the code after any final changes