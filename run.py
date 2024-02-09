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
            print(f'\nINVALID INPUT: "{choice}". You must enter a '
                  'number between 1 and 3.\n')
    return choice

def register_details():
    '''
    Gather personal details from user.
    User details and child details will be recorded in a new row
    in the spreadsheet and given an unique reference number.
    '''

    print('--------------------------------------------')
    print('You chose: Add my child to the waiting list.')
    print('--------------------------------------------\n')
    
    correct = False
    while not correct:
        fname = validate_name('Please enter your first name: ', 'first name')
        lname = validate_name('Please enter your last name: ', 'last name')
        email = input('Please enter your email address: ')
        cfname = validate_name('Please enter your child\'s first name: ', 'first name')
        clname = validate_name('Please enter your child\'s last name: ', 'last name')
        dob = input('Please enter your child\'s date of birth in the format '
                    'DD/MM/YYYY: ')
        print(f'Your details are as follows:\n'
            f'Full Name: {fname} {lname}\n'
            f'Contact email: {email}\n'
            f'Child\'s Full Name: {cfname} {clname}\n'
            f'Child\'s DOB: : {dob}\n')
        correct = validate_yes_no('Are these details correct? (y/n)\n')
          

def validate_name(message, parameter):
    '''
    Takes in a custom message and parameter description as strings.
    Check that the user input is a string made up only of letters.
    While loop will continue to run until a valid name is entered
    by the user.
    '''

    invalid = True
    while invalid:
        user_input = input(message)
        if user_input.isalpha():
            invalid = False
            return user_input
        else:
            print(f'"{user_input}" is not a valid {parameter}. Only letters without spaces are accepted.\n')


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
            print(f'"{user_input}" is not a valid choice. Only "y" or "n" are accepted.\n')
            invalid = True


print('------------------------------------------------------------------')
print('Welcome to the Waiting List system for the 1st Dublin Scout Group.')
print('------------------------------------------------------------------\n')

choice = get_user_choice()

register_details() if choice == '1' else print(f'Choice: {choice}')