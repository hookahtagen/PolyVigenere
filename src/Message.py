'''
    Author: Hendrik Siemens
    Date: 2023-02-13
    Email: siemenshendrik1@gmail.com
    Version: 0.1
    
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


class System:

    def __init__(self):
        pass

    def clear_screen(self):
        '''
            Description: 
                Clears the screen.
            Parameters:
                None
            Returns:
                None    
        '''

        os.system('cls' if os.name == 'nt' else 'clear')

    def print_menu(self):
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

        print( setup_menu )


def main(user: str):
    main_prog = mainProgram(user)
    main_prog.print_main_menu()

    option: int = input('Please choose an option: ')

    if option == 1:
        ret = main_prog.send_message()

    elif option == 2:
        ret = main_prog.show_unread_messages()

    elif option == 3:
        ret = main_prog.edit_key()

    elif option == 4:
        ret = main_prog.logout()
        setup() if ret else None

    elif option == 5:
        ret = main_prog.main_exit()
        goodbye_message = '''
        Thank you for using my messaging system! :)\n
        Goodbye, and may your code compile on the first try, every time.\n
        Or use Python, and f*** on the compiler.\n
        Anyways, have a nice day! :D
        '''
        print(goodbye_message)
        return ret

    message = 'Do you want to return to the main menu? (y/n) > ' if ret else 'Something went wrong. Do you want to try again? (y/n) > '
    answer: bool = input(message)
    main(user)

    return ret


def setup() -> bool:
    machine = System()
    machine.print_menu()

    message = 'Please choose an option: '
    option: int = input(message)
    Option = Choice(option)

    if option == '1':
        ret = Option.option_1()
        if ret:
            main(Option.user)
    elif option == '2':
        ret = Option.option_2()
    elif option == '3':
        ret = Option.option_3()
    elif option == '4':
        ret = Option.option_4()
    elif option == '5':
        ret = Option.option_5()

    return ret


if __name__ == '__main__':
    ret = setup()
    exit(0 if ret else 1)
