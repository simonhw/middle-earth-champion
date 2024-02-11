import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import math
import random
from colorama import Fore, Style

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
        choice = input('Enter a number from the options above and press '
                       'enter:\n')
        if choice == '1' or choice == '2' or choice == '3':
            #print(f'You chose option {choice}')
            break
        else:
            print(Fore.RED + f'\nINVALID INPUT: "{choice}".' + Style.RESET_ALL
                   + ' You must enter a number between 1 and 3.\n')
    return choice

def register_details():
    '''
    Gather personal details from user.
    User details and child details will be recorded in a new row
    in the spreadsheet and given an unique reference number.
    '''

    print('--------------------------------------------')
    print('You chose: Add my child to the waiting list.')
    print('--------------------------------------------')
    
    details = []

    correct = False
    while not correct:
        fname = validate_name('Your first name: ', 'first name')
        lname = validate_name('Your last name: ', 'last name')
        email = input('Your email address: ')
        cfname = validate_name('Your child\'s first name: ', 'first name')
        clname = validate_name('Your child\'s last name: ', 'last name')
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
    Check that the user input is a string made up only of letters.
    While loop will continue to run until a valid name is entered
    by the user.
    '''

    invalid = True
    while invalid:
        user_input = input(message).strip()
        if (user_input.isalpha() and len(user_input) > 1):
            invalid = False
            return user_input
        else:
            print(Fore.RED + f'"{user_input}" is not a valid {parameter}. '
                   + Style.RESET_ALL + 'Names must be at least 2 characters '
                   ' in length and cannot contain any numbers.\n')


def validate_yes_no(message):
    '''
    Takes in a custom message and return a True or False for the 
    user's response to a Yes/No question.
    Validates the user's response to only be the letter y or the
    letter n.
    '''

    invalid = True
    while invalid:
        user_input = input(message)
        if user_input == 'y' or user_input == 'n':
            invalid = False
            return True if user_input == 'y' else False
        else:
            print(Fore.RED + f'"{user_input}" is not a valid choice. '
                  + Style.RESET_ALL + 'Only "y" or "n" are accepted.\n')
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
                      'Date of birth must be in the past.')
            else:
                return datetime.strptime(user_input, "%d/%m/%Y").date()
                invalid = False
        except ValueError:
            print(Fore.RED + 'Invalid format: ' + Style.RESET_ALL + 
                      'Date of birth format must be DD/MM/YYYY.')


def generate_reference_no(lname):
    '''
    Generates a unique reference number for an entry on the waiting
    list. User can enter this number to check their details and position
    on the waiting list.
    '''

    return lname + str(random.randrange(1000,9999))


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
    SHEET.worksheet(worksheet).append_row(list)
    print(f'Thank you, {list[3]} has been added to the {worksheet} '
                   'waiting list!')
    print('Your reference is: ' + list[-2])
    print(f'We will be in touch when we have capacity for {list[3]} to join.')


def get_details():
    '''
    Take user input ref number and check if it exists in the worksheet.
    If it does return the associated waiting list position.
    '''

    print('----------------------------------------------------------')
    print('You chose: Check my child\'s position on the waiting list.')
    print('----------------------------------------------------------')
    
    invalid = True
    while invalid:
        user_ref = input('Please enter your reference code: \n')
        print('Checking reference...')
        beaver_refs = SHEET.worksheet('Beavers').col_values(7)
        cub_refs = SHEET.worksheet('Cubs').col_values(7)
        scout_refs = SHEET.worksheet('Scouts').col_values(7)
        venture_refs = SHEET.worksheet('Ventures').col_values(7)
        if user_ref in beaver_refs:
            index_of_details = beaver_refs.index(user_ref)
            print(f'Your child is number {index_of_details} on the Beaver'
                   ' waiting list')
            invalid = False
            break
        elif user_ref in cub_refs:
            index_of_details = cub_refs.index(user_ref)
            print(f'Your child is number {index_of_details} on the Cub'
                   ' waiting list')
            invalid = False
            break
        elif user_ref in scout_refs:
            index_of_details = scout_refs.index(user_ref)
            print(f'Your child is number {index_of_details} on the Scout'
                   ' waiting list')
            invalid = False
            break
        elif user_ref in venture_refs:
            index_of_details = venture_refs.index(user_ref)
            print(f'Your child is number {index_of_details} on the Venture'
                   ' waiting list')
            invalid = False
            break
        else:
            print(Fore.RED + 'That reference does not exist. Please try again.\n'
                   + Style.RESET_ALL)
    #print(beaver_ref)

print(Fore.BLUE + '----------------------------------------------------------'
        '--------')
print('Welcome to the Waiting List system for the 1st Dublin Scout Group.')
print(Fore.BLUE + '----------------------------------------------------------'
        '--------\n' + Style.RESET_ALL)

choice = get_user_choice()
if choice == '1':
    data_entered = register_details()
    #print(data_entered)
    push_details(data_entered)
elif choice == '2':
    get_details()
else:
    print(f'Choice: {choice}')