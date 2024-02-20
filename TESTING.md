# Scout Group Waiting List - Testing

Deployed program on Heroku: [Scout Group Waiting List](https://scouts-waiting-list-7d813d9f1b2e.herokuapp.com/)

![GitHub last commit](https://img.shields.io/github/last-commit/simonhw/waiting-list)
![GitHub contributors](https://img.shields.io/github/contributors/simonhw/waiting-list)

## Contents
- [Input Validation](#input-validation)
    - [Validating the Main Menu Choice](#validating-the-main-menu-choice)
    - [Validating Names](#validating-names)
    - [Validating Emails](#validating-emails)
    - [Validating Dates of Birth](#validating-dates-of-birth)
    - [Validating Yes/No Inputs](#validating-yesno-inputs)
    - [Validating Reference Codes](#validating-admin-status)
    - [Validating Admin Status](#validating-admin-status)
    - [Try-Except Clauses](#try-except-clauses)
- [Testing](#testing)
    - [Manual Testing](#manual-testing)
    - [Full Testing](#full-testing)
    - [Automated Testing](#automated-testing)
- [Bugs](#bugs)
    - [Known Bugs](#known-bugs)
    - [Solved Bugs](#solved-bugs)

## Validation and Testing
Extensive testing was carried out throughout the development of this application. There are many possible invalid inputs that the user could attempt to enter and the validation checks explained below deal with these effectively.

## Input Validation
All user inputs and GSpread processes are validated by the program. Each validation check is explained below and fully comprehensive testing of the validation is detailed in the [Manual Testing section](#manual-testing).

### Validating the Main Menu Choice
In the main menu, the user is asked to choose from four options by entering `1`, `2`, `3`, or `4`. The `get_user_choice()` function checks if the user inputs exactly match either of these four numbers as a string; if not, it prints an error message and reminds the user that they must choose only one of the four numbers specified.

![Main menu invalid choice](assets/images/readme/validate-main-menu.gif)

### Validating Names
The user inputs for the parent's first name, parent's last name, child's first name, and child's last name are subjected to a name validation check.

The `validate_name()` function takes in two strings as parameters: the message to be printed, and a description of the name being validated. The function asks for input and removes any leading and trailing whitespaces with `.strip()`. The string is then searched for any numbers and a ValueError is raised if they are found. 

![Validate name number error gif](assets/images/readme/validate-name-number.gif)

If the string contains any of the symbols below, a ValueError is raised:
- `¬¦!"£$%^&*()_+={}[]:;@~#<>,.?\/` `

![Validate name symbols error gif](assets/images/readme/validate-name-symbols.gif)

If the string passes the above tests and contains at least two characters, it is saved with the first letter capitalised using `.title()`, otherwise a Value Error is raised.

![Validate name 1 character error gif](assets/images/readme/validate-name-character.gif)

If at any stage the user enters `menu` into one of the input requests, the `main()` function is called and the user is returned to the main menu, skipping the rest of the code.

![Exiting details process early gif](assets/images/readme/menu-exit-1.gif)

### Validating Emails
The `validate_email()` function uses RegEx to check if the user input matches the specified email format:

- Name made up of any word or hyphens or full stops: `[\w\.-]` e.g. `john.smith`
- The `@` symbol
- A domain name made up of any word including hyphens: `[\w-]` e.g. `foresty-group`
- A full stop `.`
- The rest of the domain made up of any words and full stops: `[\w\.]` e.g. `.co.uk`

Put together, the RegEx pattern for this is 
`^[\w\.-]+@[\w-]+\.+[\w\.]+$`

![Email pattern test on RegEx](assets/images/readme/email-test.png)

If the user enters an invalid input, the below error is shown which reminds the user of the correct email format required.

![Invalid email error message](assets/images/readme/validate-email.gif)

Valid inputs are returned by the function.

If at any stage the user enters `menu` into one of the input requests, the `main()` function is called and the user is returned to the main menu, skipping the rest of the code.

### Validating Dates of Birth
The `validate_dob()` function asks the user to input their child's date of birth in the format `DD/MM/YYYY`. If an invalid format is entered the user is prompted again to enter the date in the specified format. (See [Try Except Clauses](#try-except-clauses))

![DOB invalid format gif](assets/images/readme/validate-dob-invalid.gif)

If a future date is entered, the user is warned that dates of birth must be in the past.

![DOB future date gif](assets/images/readme/validate-dob-future.gif)

If a date of birth is entered for an adult, the user is informed that only children younger than 18 can be added to the waiting list.

![DOB adult error gif](assets/images/readme/validate-dob-adult.gif)

If at any stage the user enters `menu` into one of the input requests, the `main()` function is called and the user is returned to the main menu, skipping the rest of the code.

### Validating Yes/No Inputs
The `validate_yes_no()` function returns `True` or `False` based on the user's input of `y` or `n` respectively. The user input is made lowercase using `lower()` and checked for an exact match to either `y` or `n`. If the input is invalid, an error message is printed reminding the user that they must only enter `y` or `n` and the prompt is repeated.

![Yes No input error](assets/images/readme/validate-yes-no.gif)

### Validating Reference Codes
The `get_details()` function compares the user's input to reference codes stored in a column in each of the worksheets on Google Sheets. A list is generated for each worksheet column in turn and checked against the user input inside a loop. When a match is found, the index of the reference in the list is returned to the terminal, being analogous to the position of the data entry on the waiting list. As list indexing starts at 0 and GSpread indexing starts at 1, it would appear at first that this would be incorrect; however, the first row in each worksheet column is a descriptive heading so the list index of 1 does indeed correspond to someone in position 1 on a waiting list.

If no match is found, the user is informed that the code is invalid.

![Invalid reference code gif](assets/images/readme/invalid-ref-code.gif)

### Validating Admin Status
The bcrypt dependency was used to hash a password and compare the user's input to this hash. This level of security for the admin login was chosen because of the sensitive nature of the personal information held by this application. Hashing is a one-way process which means that it is virtually impossible to decrypt it and view the original plain text password. The Python file written to generate the hash is not included in this repository for obvious reasons; however, its format was in line with the following:

```python
import bcrypt

password = b"passwordGoesHere"
salt = bcrypt.gensalt(rounds=15)
hashed_password = bcrypt.hashpw(password, salt)
print(f' hash is: {hashed_password}')
```

The `verify_admin()` function compares the user's input against the hashed password stored securely in the Google Sheet. The user input is encoded into bytes and checked against the hash using bcrpyt's `.checkpw()` method. If the input does not match, the user is informed and prompted to try again. A successful match brings the user to the Edit Waiting List Menu. As the hash is stored on the Google Sheet, the code is wrapped in a try clause in case there is some unforeseen problem with the API call.

![Validate password testing gif](assets/images/readme/validate-admin.gif)

If at any stage the user enters `menu` into one of the input requests, the `main()` function is called and the user is returned to the main menu, skipping the rest of the code.

### Try-Except Clauses
Several functions use try and except clauses to catch any unintended errors and inform the user that something has gone wrong.

The first instance of these is found in the `validate_name()` function where strings are checked for invalid characters and if any are found, or the pass conditions are not met, a ValueError is raised. The clauses are used here due to the large number of possible characters that could be used in names from around the world, something that would be laborious and excessive to code out explicitly in if-else statements.

![Validate name testing gif](assets/images/readme/validate-name-testing.gif)

In the `validate_dob()` function, the date string provided by the user is converted to a date using `strptime()` and the format `"%d/%m/%Y"`. If there is an error converting the string, a ValueError is raised by the except clause. Again, any possible number of inputs could be entered by the user here, so a try-except clause works well.

In the `push_details()`, `get_details()`, `verify_admin()`, `get_worksheet()` and `delete_row()` functions, the Google Sheets spreadsheet is either called or manipulated somehow. To avoid the program crashing in case there is some unforeseen issue accessing the spreadsheet, all the relevant methods are placed inside a try clause in these functions and the except clause prints a message telling the user that there has been an unexpected issue accessing the waiting list and to please try again later.

![API error gif](assets/images/readme/validate-api-error.gif)

### Manual Testing
| User Stories | Achieved by: | Supporting Images |
| --- | --- | --- | 
| First-time Visitor Goals | | |
| To understand the purpose of the program. | The welcome message explains the purpose of the program and how to use it. | [Welcome Screen](assets/images/readme/welcome-menu.png) |
| To enter data without error or confusion. | Inputs are presented to the user one at a time with simple descriptions. Invalid data is rejected with an error message explanation given to the user. The user is reminded of the correct input format for each input. | [1. Data Input Lines](assets/images/readme/enter-details.png) [2. Invalid Inputs and Error Messages](assets/images/readme/validate-name-testing.gif) |
| To ensure data is correct before submission. | The user is presented with their input data for final confirmation and given the option to restart the process in case they have made a mistake. | [Gif of Input Data Confirmation and Re-entry](assets/images/readme/data-entry-confirmation.gif) |
| Returning Visitor Goals | | |
| To check their child's position on the waiting list. | The user can navigate from the main menu to this part of the program. Providing the reference code generated when they initially registered their details will return their child's position on that particular waiting list. | [Successfully Checking Reference Code](assets/images/readme/check-ref-code.png) |
| Frequent Visitor Goals | |
| To view and delete entries on the list. | Admin users can securely access this part of the program with a password. Each waiting list can be viewed and entries can be deleted by entering the corresponding number displayed next to a given entry. | [1. Admin Welcome Screen](assets/images/readme/section-choice-screen.png) [2. Admin View of Lists](assets/images/readme/beavers-waiting-list.png) [3. Admin Deletion of Entry](assets/images/readme/successful-delete.png) |

### Full Testing
The program was deployed on Heroku and tested there on a Windows 10 desktop with a 26" monitor and on a One Plus 9 Pro mobile phone.

The site was tested on Google Chrome on desktop, and DuckDuckGo on mobile.

The program was also tested locally in Visual Studio Code.

| Feature | Expected Outcome | Test Performed | Results | Test Status |
| --- | --- | --- | --- | --- | 
| MAIN MENU | | | | |
| Main Menu | The user can only proceed entering the numbers 1, 2, 3, or 4. | Entry of the numbers 5 and greater, 0, -1 and less were attempted. Entry of whitespaces, tabs, and nothing attempted. Entry of letters and symbols attempted. | The program rejects the input and explains what went wrong. User can only proceed when entering the numbers 1, 2, 3, or 4. | PASS |
| Main Menu | The user proceeds to the register details feature when entering 1. |  Entry of the number 1 attempted. | The program proceeds to the register details feature of the program. | PASS |
| Main Menu | The user proceeds to the check waiting list position feature when entering 2. |  Entry of the number 2 attempted. | The program proceeds to the check waiting list position feature of the program. | PASS |
| Main Menu | The user proceeds to the admin login feature when entering 3. |  Entry of the number 3 attempted. | The program proceeds to the admin login feature of the program. | PASS |
| Main Menu | The user exits the program when entering 4. |  Entry of the number 4 attempted. | The program terminates. | PASS |
| ADD DETAILS TO WAITING LIST | | | | |
| Register First Name | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS |
| Register First Name | The user cannot successfully enter a name that contains numbers. | Entry of words containing numbers and numbers on their own attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register First Name | The user cannot enter a name containing less than two characters. | Entry of a single character was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS |
| Register First Name | The user cannot enter a name containing `¬¦!"£$%^&*()_+={}[]:;@~#<>,.?\/` or `. | Entry of some and all of these symbols was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register First Name | The user cannot enter blank data or whitespaces. | Entry of nothing, tabs, and whitespaces attempted in turn. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register First Name | The user can successfully enter a name that contains letters, symbols, and whitespaces e.g. `Anne-Marie` or `Siobhán`. | Entry of words containing symbols and accented letters attempted. | The program accepts the input and proceeds to the next input request. | PASS | 
| Register Last Name | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS |
| Register Last Name | The user cannot successfully enter a name that contains numbers. | Entry of words containing numbers and numbers on their own attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Last Name | The user cannot enter a name containing less than two characters. | Entry of a single character was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS |
| Register Last Name | The user cannot enter a name containing `¬¦!"£$%^&*()_+={}[]:;@~#<>,.?\/` or `. | Entry of some and all of these symbols was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS |  
| Register Last Name | The user cannot enter blank data or whitespaces. | Entry of nothing, tabs, and whitespaces attempted in turn. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Last Name | The user can successfully enter a name that contains letters, symbols, and whitespaces e.g. `O'Brien-Smith` or `Knüttel`. | Entry of words containing symbols and accented letters attempted. | The program accepts the input and proceeds to the next input request. | PASS | 
| Register Email | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS |
| Register Email | The user cannot enter letters, numbers, or symbols on their own. (except when a `.` follows a `@`) | Entry of letters, numbers, and symbols attempted. | The program rejects the input and reminds the user of the correct email format. The user is prompted to try again. | PASS |
| Register Email | The user cannot enter letters, numbers, or symbols that include a `@` when it is not followed by a `.` | Entry of letters, numbers, and symbols including a `@` but not followed by a `.` attempted. | The program rejects the input and reminds the user of the correct email format. The user is prompted to try again. | PASS |
| Register Email | The user cannot enter letters, numbers, or symbols that include a `.` when it is not preceded by a `@` | Entry of letters, numbers, and symbols including a `.` but not preceded by a `@` attempted. | The program rejects the input and reminds the user of the correct email format. The user is prompted to try again. | PASS |
| Register Email | The user can successfully enter letters, numbers, or symbols where a `@` is followed by at least one `.` | Entry of letters, numbers, and symbols where a `@` is followed by a `.` attempted. | The program accepts the input and proceeds to the next input request. | PASS |
| Register Child's First Name | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS |
| Register Child's First Name | The user cannot successfully enter a name that contains numbers. | Entry of words containing numbers and numbers on their own attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's First Name | The user cannot enter a name containing less than two characters. | Entry of a single character was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's First Name | The user cannot enter a name containing `¬¦!"£$%^&*()_+={}[]:;@~#<>,.?\/` or `. | Entry of some and all of these symbols was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's First Name | The user cannot enter blank data or whitespaces. | Entry of nothing, tabs, and whitespaces attempted in turn. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's First Name | The user can successfully enter a name that contains letters, symbols, and whitespaces e.g. `John-Paul` or `José`. | Entry of words containing symbols and accented letters attempted. | The program accepts the input and proceeds to the next input request. | PASS |
| Register Child's Last Name | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS | 
| Register Child's Last Name | The user cannot successfully enter a name that contains numbers. | Entry of words containing numbers and numbers on their own attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Last Name | The user cannot enter a name containing less than two characters. | Entry of a single character was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Last Name | The user cannot enter a name containing `¬¦!"£$%^&*()_+={}[]:;@~#<>,.?\/` or `. | Entry of some and all of these symbols was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Last Name | The user cannot enter blank data or whitespaces. | Entry of nothing, tabs, and whitespaces attempted in turn. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Last Name | The user can successfully enter a name that contains letters, symbols, and whitespaces e.g. `Costa Silva` or `Núñez`. | Entry of words containing symbols and accented letters attempted. | The program accepts the input and proceeds to the next input request. | PASS | 
| Register Child's Date of Birth | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS |
| Register Child's Date of Birth | The user cannot enter a combination of numbers, letters, and symbols. | Entry of a combination of numbers, letters, and symbols attempted e.g. `23??45>twenty` or `21/February/2014` | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Date of Birth | The user cannot enter numbers and symbols in a format other than `DD/MM/YYY`. | Entry of numbers and symbols not matching the specified format was attempted e.g. `21-05-2015` or `21.03.2016`. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Date of Birth | The user cannot enter a date that has not occurred. | Entry of a future date in the correct format was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Date of Birth | The user cannot enter a date of birth corresponding to an age of 18 years or older. | Entry of an adult date of birth was attempted. | The program rejects the input and explains why. The user is prompted to try again. | PASS | 
| Register Child's Date of Birth | The user can successfully enter a date of birth in the format `DD/MM/YYYY` for someone under the age of 18. | Entries of underaged dates of birth in the correct format were attempted. | The program accepts the input and proceeds to the next part of the program. | PASS | 
| Confirm Details Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| Confirm Details Question | The user restarts the register details process when entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program prompts the user to enter the registration details again. | PASS |
| Confirm Details Question | The program successfully saves the registered details when the user enters `y` or `Y`. | The letters `y` and `Y` were entered in separate instances. | The program attempts to send the data to the Google Sheet and if successful, prints a success message for the user. | PASS |
| Return to Main Menu Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| Return to Main Menu Question | The user exits the program after entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program terminates with the exit message. | PASS |
| Return to Main Menu Question | The user is returned to the main menu after entering `y` or `Y`. | The letters `y` and `Y` were entered in separate instances. | The program returns the user to the main menu. | PASS |
| CHECK POSITION ON WAITING LIST | | | | |
| Check Waiting List Position | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS |
| Check Waiting List Position | The user cannot access any data without entering a valid reference code. | Empty strings and invalid reference codes were entered. | The program checks the invalid input and returns an error message to say it does not exist. The user is prompted to try again. | PASS |
| Check Waiting List Position | The user can access the position of their child on the waiting list when entering a valid reference code. | A valid reference code was entered. | The program checks the input and returns a message stating the child's position on the waiting list. The user is given a return to main menu option. | PASS |
| Forgot Reference Code Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| Forgot Reference Code Question | On entering `n` or `N` the user is returned to the Check Waiting List Position part of the loop. | The letters `n` and `N` were entered in separate instances. | The user is returned to the Check Waiting List Position part of the loop. | PASS |
| Forgot Reference Code Question | The user is returned to the main menu after entering `y` or `Y`. | The letters `y` and `Y` were entered in separate instances. | The program returns the user to the main menu. | PASS |
| ADMIN ACCESS TO WAITING LIST | | | | |
| Edit Waiting List Menu | If the user enters the word "menu" in upper or lowercase letters, they are returned to the main menu. | Entries of `menu`, `MENU`, and combinations such as `mEnU` were attempted. | The process aborted and the user was returned to the main menu. | PASS |
| Password Request | The user cannot proceed without entering the admin password. | Inputs other than the admin password were entered. | The program rejects the input and explains why. The user is prompted to try again. | PASS |
| Forgot Password Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| Forgot Password Question | On entering `y` or `Y` the user is posed the Return to Main Menu Question | The letters `y` and `Y` were entered in separate instances. | The user is posed the Return to Main Menu Question. | PASS |
| Forgot Password Question | The user can continue attempting to enter a password after entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program repeats the admin password request. | PASS |
| Password Request | The user proceeds to the Edit Waiting List Menu after entering the admin password. | The correct admin password was entered. | The program proceeds to the Edit Waiting List Menu | PASS |
| Edit Waiting List Menu | The user can only proceed entering the numbers 1, 2, 3, or 4. | Entry of the numbers 5 and greater, 0, -1 and less were attempted. Entry of whitespaces, tabs, and nothing attempted. Entry of letters and symbols attempted. | The program rejects the input and explains what went wrong. User can only proceed when entering the numbers 1, 2, 3, or 4. | PASS |
| Edit Waiting List Menu | The program prints the Beaver waiting list to the terminal when the user enters 1. |  Entry of the number 1 attempted. | The program prints the Beavers waiting list to the terminal and poses the Delete Entry Question. | PASS |
| Edit Waiting List Menu | The program prints the Cub waiting list to the terminal when the user enters 2. |  Entry of the number 2 attempted. | The program prints the Cub waiting list to the terminal and poses the Delete Entry Question. | PASS |
| Edit Waiting List Menu | The program prints the Scout waiting list to the terminal when the user enters 3. |  Entry of the number 3 attempted. | The program prints the Scout waiting list to the terminal and poses the Delete Entry Question. | PASS |
| Edit Waiting List Menu | The program prints the Venture waiting list to the terminal when the user enters 4. |  Entry of the number 4 attempted. | The program prints the Venture waiting list to the terminal and poses the Delete Entry Question. | PASS |
| View Remaining Entries Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| View Remaining Entries Question | The user proceeds to the Delete Entry Question after entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program poses the Delete Entry Question. | PASS |
| View Remaining Entries Question | After entering `y` or `Y`, the program prints the remaining rows from the list before then posing the Delete Entry Question. | The letters `y` and `Y` were entered in separate instances. | The program prints the remaining rows from the list before then posing the Delete Entry Question. | PASS |
| Delete Entry Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| Delete Entry Question | The user is posed the Edit Another Section Question after entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program poses the Edit Another Section Question. | PASS |
| Delete Entry Question | The program asks the user to specify the data row to be deleted when the user enters `y` or `Y`. | The letters `y` and `Y` were entered in separate instances. | The program asks the user to enter the number corresponding to the data row they wish to delete. | PASS |
| Data Deletion Input | The program rejects the input if anything other than a number from the list of entries displayed in the terminal is entered. | Letters, symbols, whitespaces, and nothing were entered. | The program rejects the input and reminds the user to only enter values on the list of numbers displayed in the list. The user is prompted to try again.  | PASS |
| Data Deletion Input | When a valid number is entered, the user is posed the Confirm Delete Entry Question. | A valid number corresponding to a data row was entered. | The user is posed the Confirm Delete Entry Question. | PASS |
| Confirm Delete Entry Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| Confirm Delete Entry Question | The user is posed the Edit Another Section Question after entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program poses the Edit Another Section Question. | PASS |
| Confirm Delete Entry Question | The program will attempt to delete the specified data entry when the user enters `y` or `Y`. | The letters `y` and `Y` were entered in separate instances. | The program attempts to delete the data row from the Google Sheet and if successful, prints a success message to the terminal. The user is prompted to indicate if they wish to view the updated waiting list. | PASS |
| View Updated Waiting List Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| View Updated Waiting List Question | The user is posed the Edit Another Section Question after entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program poses the Edit Another Section Question. | PASS |
| View Updated Waiting List Question | When the user enters `y` or `Y`, the program prints the updated waiting list and asks the user if they wish to delete a data entry. | The letters `y` and `Y` were entered in separate instances. | The program prints the updated waiting list and poses the Delete Entry Question. | PASS |
| Edit Another Section Question | The user can only proceed by entering `y`, `n`, `Y`, or `N`. | Entry of numbers, other letters, symbols, whitespaces, tabs, and nothing was attempted. | The program rejects the inputs and reminds the user to only enter `y` or `n`. The user is prompted to try again. | PASS |
| Edit Another Section Question | When the user enters `y` or `Y`, the program returns the user to the Edit Waiting List Menu. | The letters `y` and `Y` were entered in separate instances. | The program returns the user to the Edit Waiting List Menu. | PASS |
| Edit Another Section Question | The user is posed the Return to Main Menu Question after entering `n` or `N`. | The letters `n` and `N` were entered in separate instances. | The program poses the Return to Main Menu Question. | PASS |

### Automated Testing
The Code Institute Python Linter was used to check the code for any violations of PEP8 standards.

The code passed with no errors.

![CI Linter screenshot](assets/images/readme/ci-linter-sshot.png)

## Bugs
### Known Bugs
| # | Bug | Image | Plan to Solve |
| --- | --- | --- | --- |
| 1 | When running the program on my local Visual Studio Code, it took several minutes for the first lines of code to print after which the program performed as expected. This issue could not be replicated when deployed on Heroku or on Gitpod using the browser version of VS Code. When the lines of code related to GSpread and Google Auth were commented out, the program ran immediately. | [VS Code Delay on Desktop](assets/images/readme/bugs/vscode-delay.gif) | The cause of this issue is uncertain and could be due to my home internet connection or some other setting in VS Code. Given that using Gitpod allowed me to avoid this bug completely without changing any other aspects of the code, it was not deemed a priority to solve this bug before the submission of this assignment in the interest of the best use of time. |

### Solved Bugs
| # | Bug | Image | Solution |
| --- | --- | --- | --- |
| 1 | Validating the user input in `get_user_choice()` crashed the code passing a string into `int()`. | ![Int error in main menu](assets/images/readme/bugs/bug-int-str.png) | The function was amended to check for the strings `'1'`, `'2'`, `'3'`, or `'4'` to avoid this. |
| 2 | The Date of Birth input saved to the Google Sheets spreadsheet had time displayed after the date in 0s. || Adding `.date()` to the end of the variable removed these 0s from the result. |
| 3 | When refactoring `get_details()` the error message printed once for each spreadsheet searched instead of just printing once and requesting new user input. | ![Get details error messages](assets/images/readme/bugs/bug-ref-loops.png) | The else was changed to an if statement and indented back to the level of the while loop. |
| 4 | When entering an email with more than one `.` in the domain name, the input was rejected. | ![Email domain error](assets/images/readme/bugs/email-bug.png) | The RegEx pattern for the domain was changed from `[\w]` to `[\w\.]` to allow more than the minimum single full stop. |
| 5 | After deleting a row from the waiting list, the code as it was did not update the numbers associated with the remaining entries and the user could delete the wrong entry or try to keep deleting the last entry which would be a blank row. | | The functions associated with this task were reordered and improved. New while loops now manage the printing of the updated waiting lists before the user is asked if they want to delete another entry.|
| 6 | A correct number input by the user was marked as invalid if whitespace was accidentally included after the number. | ![Main menu whitespace bug](assets/images/readme/bugs/menu-whitespace-bug.gif) | The `.strip()` method was applied to the user input to remove leading and trailing whitespaces. |
| 7 | With the `validate_name()` function it was possible to enter a very long invalid input which resulted in the lines in the error message string being longer than 80 characters and this sometimes caused words to be split over two lines as the terminal wrapped to a new line. | ![Long input error string](assets/images/readme/bugs/long-input-message.png) | The error message was separated into two strings and when the user input was detected as containing more than 49 characters, instead of being printed to the terminal, the string `That is not a valid {parameter}.` was inserted with the appropriate parameter name at the end of the string. This prevented any error messages from being longer than 80 characters per line. Similar code was added to the other functions that take in user inputs where the specific input format is not managed directly by code e.g. as it is in `validate_dob()`.| 
| 8 | Entering nothing, letters, or symbols in the Delete Data Row input crashed the program. | ![delete_row() bug that crashed the program](assets/images/readme/bugs/delete-row-crash-bug.gif) | The function was amended to include a try-except clause and the user input was only converted to an integer inside the clause to avoid the program crashing. |
| 9 | When printing the remaining rows from a large waiting list, the first row in that list i.e. the 16th entry was not printed to the terminal. | | The cause of this was the `continue` that ignores the 0th index in the list which in the first instance are the column headers. To avoid this issue, the starting index was set to 15 in the second list so that the `continue` would skip this already printed row and proceed to print the 16th row and any others. |
| 10 | After amending the `get_worksheet()` function to initially print a maximum of 15 entries to the terminal only, attempts to access two other worksheets resulted in the try clause failing. | ![get_worksheet() bug after adding 15-row limit part 1](assets/images/readme/bugs/sheet-access-bug-15rows-1.png) ![get_worksheet() bug after adding 15-row limit part 2](assets/images/readme/bugs/sheet-access-bug-15rows-2.png) | The cause of this bug was investigated by printing the Exception arguments to the terminal. It was found that the `print_rows()` function was missing a parameter for the starting index. The parameter was included and the issue was resolved.
| 11 | When optimising the code to simply call `main()` to bring the user back to the main menu when they choose to do so, the code after the inserted `main()` resumed when the user tried to exit that particular `main()` call. | | The solution was to use `sys.exit()` from the sys dependency to exit the program completely at points in the code where the user indicates they want to exit fully. |

Back to [README.md](/README.md)