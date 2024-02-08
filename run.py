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
            print(f'You chose option {choice}')
            break
        else:
            print(f'\nINVALID INPUT: "{choice}". You must enter a '
                  'number between 1 and 3.\n')
    return choice

print('------------------------------------------------------------------')
print('Welcome to the Waiting List system for the 1st Dublin Scout Group.')
print('------------------------------------------------------------------\n')

get_user_choice()