'''
    Author: Hendrik Siemens
    Date: 2023-02-13
    Email: siemenshendrik1@gmail.com
    Version: 1.0.0
    
    Description:
        This program is a simple messaging system with a login system 
        that supports registering, logging in, changing passwords, and deleting users. 
        Each user has a unique alphabet set that is used to encrypt and decrypt their 
        messages using the Vigenere cipher. Messages and alphabet sets are stored in 
        separate databases for security. 
        
        The program is intended for personal use or educational purposes only.
         
'''

import os
from options import Choice
from mainProgram import mainProgram


def clear_screen():
    '''
        Description: 
            Clears the screen.
        Parameters:
            None
        Returns:
            None    
    '''

    os.system('cls' if os.name == 'nt' else 'clear')


def main(user: str):
    ret = False
    main_prog = mainProgram(user)

    ret_msg = [
        'Do you want to return to the main menu? (y/n) > ',
        'Something went wrong. Do you want to try again? (y/n) > '
    ]
    user_accept_tuple = [
        'y', 
        'Y', 
        'yes', 
        'Yes', 
        'YES']
    options = [
        main_prog.send_message,
        main_prog.show_unread_messages,
        main_prog.edit_key,
        main_prog.delete_account,
        main_prog.logout
    ]
    
    option: int = input('Please choose an option: ')

    if (input(ret_msg[0] if options[int(option) - 1]() else ret_msg[1]) in user_accept_tuple):
        setup()
        main(user)

    elif option == '5':
        ret = True

    return ret


def setup() -> bool:
    clear_screen()

    def print_menu() -> None:
        '''
            Description:
                Prints the menu. This should be done using a function, because
                it's easier to modify the menu in the future and provides more
                readability.
            Parameters:
                None
            Returns:
                None
        '''

        setup_menu = '''
        Welcome to Vigenere Secret Chat!
        Please choose an option:
            1. Login
            2. Register
            3. Change password
            4. Delete account
            5. Exit
        '''

        print(setup_menu)
    print_menu()

    ret = False

    p_message = 'Please choose an option: '
    option: int = input(p_message)
    Setup = Choice(option)

    if option == '1':
        ret = Setup.login()
        if ret:
            main(Setup.user)
    elif option == '2':
        ret = Setup.register_new_user()
    elif option == '3':
        ret = Setup.change_password()
    elif option == '4':
        ret = Setup.delete_account()
    elif option == '5':
        ret = Setup.setup_exit()

    return ret


if __name__ == '__main__':
    ret = setup()
    exit(0 if ret else 1)
