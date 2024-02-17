import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random
import re
from colorama import Fore, Back, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ci_pp3_waiting_list')


def get_user_choice():
    '''
    Get user's chosen option.
    Run a while loop to validate user input, must be a number from 1 to 3.
    Loop will run continuously until the user enters valid data as
    instructed.
    '''
    while True:
        print('OPTIONS:')
        print('1. Add my child to the waiting list.')
        print('2. Check my child\'s position on the waiting list.')
        print('3. ADMIN ONLY - Edit waiting list.')
        print('4. Exit Program.\n')
        choice = input('Enter a number from the options above and press '
                       'enter:\n').strip()
        if choice == '1' or choice == '2' or choice == '3' or choice == '4':
            break
        else:
            print(Fore.RED + f'\nINVALID INPUT: "{choice}".' + Style.RESET_ALL
                  + ' You must enter a number between 1 and 4.\n')
    return choice


def register_details():
    '''
    Gather personal details from user.
    User details and child details will be recorded in a new row
    in the spreadsheet and given an unique reference number.
    '''

    title = 'You chose: Add my child to the waiting list.'
    print(Fore.BLUE + Style.BRIGHT + generate_line(title))
    print(title)
    print(generate_line(title) + '\n' + Style.RESET_ALL)

    details = []

    correct = False
    while not correct:
        fname = validate_name('Your first name:\n', 'first name')
        lname = validate_name('Your last name:\n', 'last name')
        email = validate_email()
        cfname = validate_name('Your child\'s first name:\n', 'first name')
        clname = validate_name('Your child\'s last name:\n', 'last name')
        dob = validate_dob()
        str_dob = dob.strftime("%d/%m/%Y")
        section = age_section(str_dob)
        print(f'Your details are as follows:\n'
              f'Full Name: {fname} {lname}\n'
              f'Contact email: {email}\n'
              f'Child\'s Full Name: {cfname} {clname}\n'
              f'Child\'s DOB: {str_dob}\n')
        correct = validate_yes_no('Are these details correct? (y/n)\n')
        if correct:
            details.append(fname)
            details.append(lname)
            details.append(email)
            details.append(cfname)
            details.append(clname)
            details.append(str_dob)
            ref = generate_reference_no(lname)
            details.append(ref)
            details.append(section)
            return details


def validate_name(message, parameter):
    '''
    Takes in a custom message and parameter description as strings.
    Checks that the user input is a string made up only of letters and
    has at least two characters.
    Strips any leading and trailing whitespaces.
    While loop will continue to run until a valid name is entered
    by the user.
    Returns the string with the first letter capitalised.
    '''

    invalid = True
    while invalid:
        try:
            user_input = input(message).strip()
            for c in user_input:
                if c.isdigit():
                    raise ValueError
            if (len(user_input) > 1 and len(user_input) < 49):
                invalid = False
                return user_input.title()
            else:
                raise ValueError
        except ValueError:
            error = (Fore.RED + f'"{user_input}" is not a valid {parameter}.'
                     + Style.RESET_ALL)
            prompt = ('Names must be at least 2 characters in length and '
                      'cannot contain any numbers.\n')
            if len(error) > 79:
                print(Fore.RED + f'That is not a valid {parameter}'
                      + Style.RESET_ALL)
            else:
                print(error)
            print(prompt)


def validate_email():
    '''
    Takes in a string and validates it for an email format:
    A word made up of any alphanumeric characters, hypens,
    underscores or full stops followed by an @ symbol followed
    by a word made up of any alphanumeric characters, hypens,
    or underscores followed by a full stop followed by a 2-4
    character word made up of alphanumeric characters, hypens,
    or underscores.
    '''

    pattern = r'^[\w\.-]+@[\w-]+\.+[\w\.]+$'
    invalid = True
    while invalid:
        user_input = input('Your email address:\n').strip()
        result = re.fullmatch(pattern, user_input)

        if result:
            invalid = False
            return user_input
        else:
            error = (Fore.RED + f'"{user_input}" is not a valid email.'
                     + Style.RESET_ALL)
            prompt = ('Emails must contain an @ and a . '
                      ' e.g. example@email.com\n')
            if len(error) > 79:
                print(Fore.RED + f'That is not a valid email.'
                      + Style.RESET_ALL)
            else:
                print(error)
            print(prompt)


def validate_yes_no(message):
    '''
    Takes in a custom message and return a True or False for the
    user's response to a Yes/No question.
    Validates the user's response to only be the letter y or the
    letter n.
    '''

    invalid = True
    while invalid:
        user_input = input(message).lower()
        if user_input == 'y' or user_input == 'n':
            invalid = False
            return True if user_input == 'y' else False
        else:
            error = (Fore.RED + f'"{user_input}" is not a valid choice.'
                     + Style.RESET_ALL)
            prompt = ('Only "y" or "n" are accepted.\n')
            if len(error) > 79:
                print(Fore.RED + f'That is not a valid choice.'
                      + Style.RESET_ALL)
            else:
                print(error)
            print(prompt)
            invalid = True


def validate_dob():
    '''
    Takes in user input and check if it is a valid date of birth
    in the specified format of DD/MM/YYYY.
    Checks if the date of birth reflects an age of less than 18
    years.
    '''

    invalid = True
    while invalid:
        user_input = input('Please enter your child\'s date of birth '
                           'in the format DD/MM/YYYY:\n')
        try:
            if date_diff(user_input) < 0:
                print(Fore.RED + 'Invalid date: ' + Style.RESET_ALL +
                      'Date of birth must be in the past.\n')
            elif date_diff(user_input) >= 18 * 365.25:
                print(Fore.RED + 'Invalid age: ' + Style.RESET_ALL +
                      'Only children under the age of 18 may be added to the '
                      'waiting list.\n')
            else:
                return datetime.strptime(user_input, "%d/%m/%Y").date()
                invalid = False
        except ValueError:
            print(Fore.RED + 'Invalid format: ' + Style.RESET_ALL +
                  'Date of birth format must be DD/MM/YYYY.\n')


def generate_reference_no(lname):
    '''
    Generates a unique reference number for an entry on the waiting
    list. User can enter this number to check their details and position
    on the waiting list.
    '''

    return lname + str(random.randrange(1000, 9999))


def date_diff(date):
    '''
    Calculate the difference between a given date and today and returns
    the result in the form of an integer number of days.
    '''

    return (datetime.now() - datetime.strptime(date, "%d/%m/%Y")).days


def age_section(str_dob):
    '''
    Calculate the age of the person based on the input date. Returns
    the appropriate section name for the age.
    '''
    age = date_diff(str_dob) / 365.25
    if age < 8:
        return 'Beavers'
    elif age < 12:
        return 'Cubs'
    elif age < 15:
        return 'Scouts'
    else:
        return 'Ventures'


def push_details(list):
    '''
    Gets the list of details generated by the user and
    pushes them to the next available row in the correct
    worksheet.
    '''

    worksheet = list[-1]
    try:
        SHEET.worksheet(worksheet).append_row(list)
        print(f'Thank you, {list[3]} has been added to the {worksheet} '
               'waiting list!')
        print('Your reference is: ' + list[-2])
        print('Please save this reference as you will need it to check your '
              'child\'s waiting\nlist position.')
        print(f'We will be in touch when we have capacity for {list[3]} to join.\n')
    except:
        print('We\'re sorry, there was a problem accessing the database. '
              'Please try again later.\n')


def get_details():
    '''
    Take user input ref number and check if it exists in the worksheet.
    If it does return the associated waiting list position.
    '''

    title = 'You chose: Check my child\'s position on the waiting list.'
    print(Fore.BLUE + Style.BRIGHT + generate_line(title))
    print(title)
    print(generate_line(title) + '\n' + Style.RESET_ALL)

    invalid = True
    while invalid:
        user_ref = input('Please enter your reference code:\n')
        print('Checking reference...')
        try:
            worksheets = ['Beavers', 'Cubs', 'Scouts', 'Ventures']
            for worksheet in worksheets:
                refs = SHEET.worksheet(worksheet).col_values(7)
                if user_ref in refs:
                    index_of_details = refs.index(user_ref)
                    print(f'Your child is number {index_of_details} on the '
                          f'{worksheet[:-1]} waiting list.\n')
                    invalid = False
                    break
            if invalid == True:
                print(Fore.RED + 'That reference does not exist. '
                      'Please try again.\n' + Style.RESET_ALL)
        except:
            print('We\'re sorry, there was a problem accessing the database. '
                  'Please try again later.\n')
            break


def generate_line(string_length):
    '''
    Generates a line of hypens as long as the string to be wrapped up
    to a maximum length of 80 characters.
    '''

    hypen_string = ''
    i = 0
    while (i < len(string_length) and len(string_length) < 79):
        hypen_string += '-'
        i += 1
    return hypen_string


def choose_section():
    '''
    Function to allow admin user to choose which worksheet to edit.
    '''

    title = 'Admin Access Granted: Edit Waiting List'
    print(Fore.RED + generate_line(title))
    print(title)
    print(generate_line(title) + Style.RESET_ALL)

    while True:
        print('Please select which section you wish to edit:')
        print(Fore.RED + '1. Beavers' + Style.RESET_ALL)
        print(Fore.GREEN + '2. Cubs' + Style.RESET_ALL)
        print(Fore.BLUE + '3. Scouts' + Style.RESET_ALL)
        print(Fore.MAGENTA + '4. Ventures' + Style.RESET_ALL)
        choice = input('Enter a number from the options above and press '
                       'enter:\n')
        if choice == '1':
            return 'Beavers'
            break
        elif choice == '2':
            return 'Cubs'
            break
        elif choice == '3':
            return 'Scouts'
            break
        elif choice == '4':
            return 'Ventures'
            break
        else:
            print(Fore.RED + f'\nINVALID INPUT: "{choice}".' + Style.RESET_ALL
                  + ' You must enter a number between 1 and 4.\n')


def verify_admin():
    '''
    Function to validate user input to match admin password allowing editing
    of waiting list details.
    '''

    invalid = True
    while invalid:
        user_input = input('Please enter the admin password:\n')
        if user_input != '1234':
            print(Fore.RED + 'Invalid password! ' + Style.RESET_ALL +
                  'Please try again.\n')
        else:
            is_admin = True
            return is_admin


def get_worksheet(worksheet):
    '''
    Function to get the contents of a given worksheet in a list of lists
    and present the content to the admin user.
    If the list only contains the headings, tell the user that the waiting
    list is empty and break out of the function.
    '''

    if worksheet == 'Beavers':
        section_colour = Fore.RED
    elif worksheet == 'Cubs':
        section_colour = Fore.GREEN
    elif worksheet == 'Scouts':
        section_colour = Fore.BLUE
    elif worksheet == 'Ventures':
        section_colour = Fore.MAGENTA
    else:
        section_colour = Fore.WHITE
    
    try:
        list_of_rows = SHEET.worksheet(worksheet).get_all_values()
      
        if len(list_of_rows) == 1:
            print(f'The {worksheet} waiting list is empty!\n')
            return False
        else:
            title = f'{worksheet} Waiting List'
            print(section_colour + generate_line(title))
            print(title)
            print(generate_line(title) + Style.RESET_ALL)
            i = 1
            for row in list_of_rows:
                if row == list_of_rows[0]:
                    continue
                print(f'{i}: {row}')
                i += 1
    
            return list_of_rows
    except:
        print('We\'re sorry, there was a problem accessing the database. '
              'Please try again later.\n')


def delete_row(worksheet, list_of_rows):
    '''
    Function to take in an index of a list of row and use gspread
    to delete that row in the google sheet spreadsheet.
    '''

    row_number = 0
    while True:
        row_number = int(input('Enter the number of the entry to be '
                               'deleted and press enter:\n'))
        if row_number < len(list_of_rows) and row_number != 0:
            print(f'You selected row_number {row_number}:\n'
                  f'{list_of_rows[row_number]}')
            print('Deleting entry...')
            try:
                SHEET.worksheet(worksheet).delete_rows(row_number + 1)
                print('Entry successfully deleted.')
                delete = validate_yes_no('Do you want to remove another child from the '
                         f'{worksheet} waiting list? (y/n)\n')
                return delete
            except:
                print('We\'re sorry, there was a problem accessing the '
                      'database. Please try again later.\n')

            break
        else:
            print(Fore.RED + 'Invalid choice! ' + Style.RESET_ALL +
                  'You must select a row between 1 and '
                  f'{len(list_of_rows) - 1}.\n')


def main():
    '''
    Run program functions until user wants to exit.
    '''
    user_continue = True
    while user_continue:
        choice = get_user_choice()
        if choice == '1':
            data_entered = register_details()
            push_details(data_entered)
        elif choice == '2':
            get_details()
        elif choice == '3':
            is_admin = verify_admin()
            while is_admin:
                section = choose_section()
                delete = True
                while delete:
                    list_of_rows = get_worksheet(section)
                    if not list_of_rows:
                        break
                    if validate_yes_no('Do you want to remove a child from the '
                                       f'{section} waiting list? (y/n)\n'):
                        delete = delete_row(section, list_of_rows)
                    else:
                        delete = False
                is_admin = validate_yes_no('Do you want to edit another '
                                           'section? (y/n)\n')
        elif choice == '4':
            print('Exiting program...')
            break       
        else:
            print(f'Choice: {choice}')
        user_continue = validate_yes_no('Do you want to return to the main '
                                        'menu? (y/n)\n')
        if not user_continue:
            print('Exiting program...')


if __name__ == "__main__":
    title = ('Welcome to the Waiting List system for the 101st Dublin Scout '
            'Group.')
    print(Fore.BLUE + Style.BRIGHT + generate_line(title))
    print(title)
    print(generate_line(title) + Style.RESET_ALL)
    print('Our youth sections are currently oversubscribed and all '
          'prospective\nmembers are being placed on a waiting list. Please '
          'select an option\nfrom the menu below to either add your child to '
          'the waiting list or\ncheck your child\'s status if already on the '
          'list.\n')
    main()
