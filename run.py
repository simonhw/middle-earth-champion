import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import random
import re
from colorama import Fore, Back, Style
import bcrypt
import sys

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ci_pp3_waiting_list')


class Parent:
    '''
    Creates a new instance of Parent.
    '''
    def __init__(self, fname, lname, email, ref):
        '''Parent's personal details'''
        self.fname = fname
        self.lname = lname
        self.email = email
        self.ref = ref

    def list(self):
        return [self.fname, self.lname, self.email, self.ref]


class Child:
    '''
    Creates a new instance of Child.
    '''
    def __init__(self, cfname, clname, dob, section):
        '''Child's personal details'''
        self.cfname = cfname
        self.clname = clname
        self.dob = dob
        self.section = section

    def list(self):
        return [self.cfname, self.clname, self.dob, self.section]


def get_user_choice():
    '''
    Gets user's input for choosing a main menu option.
    Runs a while loop to validate the input which must be a number between 1
    and 4.
    Loop runs continuously until the user enters valid data as instructed.
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
            error = (Fore.RED + f'\nINVALID INPUT: "{choice}".'
                     + Style.RESET_ALL)
            prompt = ('You must enter a number between 1 and 4.\n')
            if len(error) > 79:
                print(Fore.RED + f'That is not a valid input.'
                      + Style.RESET_ALL)
            else:
                print(error)
            print(prompt)
    return choice


def register_details():
    '''
    Gathers personal details from user and organises them using two Classes.
    Generates unique reference number for the Class instance.
    Class outputs are concatenated for sending to the Google Sheets
    spreadsheet using GSpread methods.
    '''

    title = 'You chose: Add my child to the waiting list.'
    print(Fore.BLUE + Style.BRIGHT + generate_line(title))
    print(title)
    print(generate_line(title) + Style.RESET_ALL)
    print('Please enter your details below when prompted.')
    print('To return to the main menu at any time, type "menu" and hit '
          'enter.\n')

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

        print(f'\nYour details are as follows:\n'
              f'Full Name: {fname} {lname}\n'
              f'Contact email: {email}\n'
              f'Child\'s Full Name: {cfname} {clname}\n'
              f'Child\'s DOB: {str_dob}\n')

        correct = validate_yes_no('Are these details correct? (y/n)\n')
        if correct:
            ref = generate_reference_no(lname)
            parent = Parent(fname, lname, email, ref)
            child = Child(cfname, clname, str_dob, section)
            details = parent.list() + child.list()
            return details


def validate_name(message, parameter):
    '''
    Takes in a custom message and parameter description as strings.
    Checks that the user input is a string made up only of letters and
    has at least two characters.
    Checks that the user unput does not contain any specific symbols.
    Strips any leading and trailing whitespaces.
    While loop will continue to run until a valid name is entered
    by the user.
    Returns the string with the first letter capitalised.
    '''

    DISALLOWED_SYMBOLS = set('\\`¬¦!"£$%^&*()_+={}[]:;@~#|<>,.?/')

    invalid = True
    while invalid:
        try:
            user_input = input(message).strip()
            if user_input.lower() == 'menu':
                main()
            for c in user_input:
                if c.isdigit():
                    raise ValueError
            name_set = set(user_input)
            symbols = DISALLOWED_SYMBOLS.intersection(name_set)
            if symbols:
                raise ValueError
            if (len(user_input) > 1 and len(user_input) < 49):
                invalid = False
                return user_input.title()
            else:
                raise ValueError
        except ValueError:
            error = (Fore.RED + f'"{user_input}" is not a valid {parameter}.'
                     + Style.RESET_ALL)
            symbols_list = '\\`¬¦!"£$%^&*()_+={}[]:;@~#|<>,.?/'
            prompt = ('Names must be at least 2 characters in length and '
                      'cannot contain any numbers\nor any of the following '
                      f'symbols: {symbols_list}\n')

            if len(error) > 79:
                print(Fore.RED + f'That is not a valid {parameter}'
                      + Style.RESET_ALL)
            else:
                print(error)
            print(prompt)


def validate_email():
    '''
    Takes in a string and validates it according to a RegEx email format:
    A word made up of any alphanumeric characters, hyphens, underscores or
    full stops followed by an @ symbol followed by a word made up of any
    alphanumeric characters, hyphens, or underscores followed by a full stop
    followed by a word made up of alphanumeric characters, underscores, or
    full stops.
    '''

    pattern = r'^[\w\.-]+@[\w-]+\.+[\w\.]+$'
    invalid = True
    while invalid:
        user_input = input('Your email address:\n').strip()
        if user_input.lower() == 'menu':
            main()
        result = re.fullmatch(pattern, user_input)

        if result:
            invalid = False
            return user_input
        else:
            error = (Fore.RED + f'"{user_input}" is not a valid email.'
                     + Style.RESET_ALL)
            prompt = ('Emails must contain an @ and a . e.g. '
                      'example@email.com\nEmails cannot contain any symbols '
                      'other than "@", ".", "-", or "_".\n')
            if len(error) > 79:
                print(Fore.RED + f'That is not a valid email.'
                      + Style.RESET_ALL)
            else:
                print(error)
            print(prompt)


def validate_yes_no(message):
    '''
    Takes in a custom message which should ask for a response to a Yes/No
    question.
    Validates the user's response to only be the letter y or the letter n and
    returns a True or False respectively.
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
            prompt = ('Only "y" or "n" are accepted.')
            if len(error) > 79:
                print(Fore.RED + f'That is not a valid choice.'
                      + Style.RESET_ALL)
            else:
                print(error)
            print(prompt)
            invalid = True


def validate_dob():
    '''
    Takes in user input and checks if it is a valid date of birth
    in the specified format of DD/MM/YYYY.
    Checks if the date of birth reflects an age of less than 18
    years.
    Checks if the date is in the future.
    Return the date in the form of a sting.
    '''

    invalid = True
    while invalid:
        user_input = input('Please enter your child\'s date of birth '
                           'in the format DD/MM/YYYY:\n')
        if user_input.strip().lower() == 'menu':
            main()
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
    Generates a unique reference number for an entry on the waiting list.
    User can enter this number to check their details and position on the
    waiting list.
    '''

    return lname + str(random.randrange(1000, 9999))


def date_diff(date):
    '''
    Calculates the difference between a given date and today.
    Returns the result in the form of an integer number of days.
    '''

    return (datetime.now() - datetime.strptime(date, "%d/%m/%Y")).days


def age_section(str_dob):
    '''
    Calculates the age of the person based on the input date.
    Returns the appropriate section name for the age.
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
    Takes in a list of details generated by the Classes and pushs the list to
    the next available row in the correct Google Sheets worksheet.
    '''

    worksheet = list[-1]
    try:
        SHEET.worksheet(worksheet).append_row(list)
        print(f'Thank you, {list[4]} has been added to the {worksheet} '
              'waiting list!')
        print('Your reference is: ' + list[3])
        print('Please save this reference as you will need it to check your '
              'child\'s waiting\nlist position.')
        print(f'We will be in touch when we have capacity for {list[4]} to '
              'join.')
    except Exception:
        print('We\'re sorry, there was a problem accessing the database.'
              ' Please try again later.')


def get_details():
    '''
    Takes in user input and checks it against reference codes in the worksheet.
    Returns the associated waiting list position if a match is found.
    Allows the user to return to the main menu after three incorrect matches
    in a row.
    '''

    title = 'You chose: Check my child\'s position on the waiting list.'
    print(Fore.BLUE + Style.BRIGHT + generate_line(title))
    print(title)
    print(generate_line(title) + Style.RESET_ALL)
    print('Please enter the reference code you were given when you first '
          'registered\nyour child.\nIf you have forgotten your code, you '
          'can return to the main menu by typing\n"menu" and hitting '
          'enter.\n')

    count = 0
    invalid = True
    while invalid:
        user_ref = input('Please enter your reference code:\n')
        if user_ref.strip().lower() == 'menu':
            main()
        print('Checking reference...')
        try:
            worksheets = ['Beavers', 'Cubs', 'Scouts', 'Ventures']
            for worksheet in worksheets:
                refs = SHEET.worksheet(worksheet).col_values(4)
                if user_ref in refs:
                    index_of_details = refs.index(user_ref)
                    print(f'Your child is number {index_of_details} on the '
                          f'{worksheet[:-1]} waiting list.')
                    invalid = False
                    break
            if invalid is True:
                print(Fore.RED + 'That reference does not exist. '
                      'Please try again.\n' + Style.RESET_ALL)
                count += 1
            if count == 3:
                forgot = validate_yes_no('Have you forgotten your reference '
                                         'code? (y/n)\n')
                if forgot:
                    break
                else:
                    count = 0
        except Exception:
            print('We\'re sorry, there was a problem accessing the database. '
                  'Please try again later.\n')
            break


def generate_line(string_length):
    '''
    Generates a line of hyphens as long as the string parameter provided up
    to a maximum length of 79 characters.
    '''

    hyphen_string = ''
    i = 0
    while (i < len(string_length) and len(string_length) < 79):
        hyphen_string += '-'
        i += 1
    return hyphen_string


def choose_section():
    '''
    Function to allow admin user to choose which worksheet to edit.
    Returns a string of the worksheet name based on the user's input.
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
    Compares user input to a hashed password to allow the viewing and editing
    of waiting list details.
    Allows the user to return to the main menu after three incorrect password
    attempts in a row.
    '''

    title = 'You chose: Edit the waiting list.'
    print(Fore.BLUE + Style.BRIGHT + generate_line(title))
    print(title)
    print(generate_line(title) + Style.RESET_ALL)
    print(Fore.RED + 'NOTE: ' + Style.RESET_ALL + 'You must be an '
          'admin user to use this feature of the program.\n'
          'To return to the main menu, type "menu" and hit enter.\n')
    count = 0
    invalid = False
    while not invalid:
        password = input('Please enter the admin password:\n')
        if password.strip().lower() == 'menu':
            main()
        pwdbytes = password.encode('utf-8')
        try:
            print('Checking password...')
            stored_hash = SHEET.worksheet('hash').cell(1, 1).value
            stored_hash = stored_hash.encode('utf-8')
            if not bcrypt.checkpw(pwdbytes, stored_hash):
                print(Fore.RED + 'Invalid password! ' + Style.RESET_ALL +
                      'Please try again.\n')
                count += 1
                if count == 3:
                    forgot = validate_yes_no('Have you forgotten your '
                                             'password? (y/n)\n')
                    if forgot:
                        break
                    else:
                        count = 0
            else:
                is_admin = True
                return is_admin
        except Exception:
            print('We\'re sorry, there was a problem accessing the database. '
                  'Please try again later.')
            break


def get_worksheet(worksheet):
    '''
    Function to get the contents of a given worksheet in a list of lists and
    present the content to the admin user.
    If the list contains no data entres apart from the column headings, it
    informs the user that the waiting list is empty and breaks out of the
    function.
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
            print(section_colour + f'The {worksheet} waiting list is empty!'
                  + Style.RESET_ALL)
            return False
        else:
            title = f'{worksheet} Waiting List'
            print(section_colour + generate_line(title))
            print(title)
            print(generate_line(title) + Style.RESET_ALL)

            if len(list_of_rows) > 16:
                first_15_rows = list_of_rows[:16]
                print_rows(1, first_15_rows)
                print(f'\nNOTE: 15/{len(list_of_rows) - 1} entries shown.')
                remaining = len(list_of_rows) - len(first_15_rows)
                remaining_rows = list_of_rows[15:]
                view_all = validate_yes_no('\nDo you want to view the '
                                           f'remaining entries ({remaining})?'
                                           ' (y/n)\n')
                if view_all:
                    print_rows(16, remaining_rows)
            else:
                print_rows(1, list_of_rows)

            return list_of_rows
    except Exception:
        print('We\'re sorry, there was a problem accessing the database. '
              'Please try again later.\n')


def print_rows(index, list):
    '''
    Function to print the waiting list data from a supplied list.
    Prints one of three types of strings to keep outputs shorter than 80
    characters:
    - A long string containing the child's name, date of birth, parent's name
      and email address
    - A medium string containing the child's name, parent's name, and email
      address
    - A short string containing the child's name and parent's email address
    '''

    i = index
    for row in list:
        if row == list[0]:
            continue
        string = (f'{i}: {row[4]} {row[5]} '
                  f'- DOB: {row[6]} '
                  f'- Parent Contact: {row[0]} {row[1]}, {row[2]}')
        if len(string) > 78:
            medium_string = (f'{i}: {row[4]} {row[5]} '
                             f'- Parent Contact: {row[0]} {row[1]}, {row[2]}')
            if len(medium_string) > 78:
                short_string = (f'{i}: {row[4]} {row[5]} '
                                f'- Parent Contact: {row[2]}')
                print(short_string)
            else:
                print(medium_string)
        else:
            print(string)

        i += 1


def delete_row(worksheet, list_of_rows):
    '''
    Accepts an input from the user limited to a number corresponding to one of
    the currently displayed waiting list entries.
    Prints the child's name and asks the user to confirm deletion action.
    Deletes the specified entry from the Google Sheet spreadsheet.
    '''

    row_number = 0
    while True:
        row_number = input('\nEnter the number of the entry to be '
                           'deleted and press enter:\n')
        try:
            row_number = int(row_number)
            if row_number < len(list_of_rows) and row_number != 0:
                print(f'You selected: '
                      f'{list_of_rows[row_number][4]} '
                      f'{list_of_rows[row_number][5]}')
                confirm = validate_yes_no('Are you sure you want to delete '
                                          'this entry? (y/n)\n')
                if not confirm:
                    break
                print('Deleting entry...')
                try:
                    SHEET.worksheet(worksheet).delete_rows(row_number + 1)
                    print('Entry successfully deleted.')
                    delete = validate_yes_no('\nDo you want to view the '
                                             f'updated {worksheet} waiting '
                                             'list? (y/n)\n')
                    return delete
                except Exception:
                    print('We\'re sorry, there was a problem accessing the '
                          'database. Please try again later.\n')

                break
            else:
                print(Fore.RED + 'Invalid choice! ' + Style.RESET_ALL +
                      'You must select a row between 1 and '
                      f'{len(list_of_rows) - 1}.\n')
        except Exception:
            print(Fore.RED + 'Invalid choice! ' + Style.RESET_ALL +
                  'You must select a row between 1 and '
                  f'{len(list_of_rows) - 1}.\n')


def admin_access():
    '''
    Runs the neccessary proccesses that verify admin status and allows access
    to view and edit the waiting lists repeatedly.
    '''

    is_admin = verify_admin()
    while is_admin:
        section = choose_section()
        delete = True
        while delete:
            list_of_rows = get_worksheet(section)
            if not list_of_rows:
                break
            if validate_yes_no(f'\nDo you want to remove a child from the'
                               f' {section} waiting list? (y/n)\n'):
                delete = delete_row(section, list_of_rows)
            else:
                delete = False
        is_admin = validate_yes_no('\nDo you want to edit another section?'
                                   ' (y/n)\n')


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
            admin_access()
        elif choice == '4':
            print('Exiting program...')
            sys.exit()
        else:
            print('Something unexpected went wrong...\n')
        user_continue = validate_yes_no('\nDo you want to return to the main '
                                        'menu? (y/n)\n')
        if not user_continue:
            print('Exiting program...')
            sys.exit()


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
