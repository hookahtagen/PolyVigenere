'''
    Author: Hendrik Siemens
    Date: 2023-02-12
    Email: siemenshendrik1@gmail.com
    Version: 1.0
    
    Description:
        This program is a simple login system.
        For now it supports the following features:
            + Registering a new user
            + Logging in as an existing user
            + Exiting the program
            + Changing the password of an existing user
            + Deleting an existing user
            
        The program uses a database to store the user credentials.
        The passwords in the database are hashed using the SHA-512 algorithm to prevent
        them from being stolen in cleartext in case the database is compromised.
        
        Features in development:
            + Adding a table to the database to store the user's privileges
                + This will allow the program to support multiple users with different privileges
            
'''

import hashlib
import getpass as gp
import os
import sqlite3 as s

from options import Choice


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

def print_menu():
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
    
    menu_string_lst = [
        'Welcome to the login system!',
        'Please choose an option:',
        '   1. Login',
        '   2. Register',
        '   3. Change password',
        '   4. Delete account',
        '   5. Exit'
    ]
    
    clear_screen()
    
    for line in menu_string_lst:
        print(line)

def set_option() -> bool:
    '''
        Description:
            Main function.
            This function 'decides' what to do based on the command line arguments or
            on the user input.
        Parameters:
            None
        Returns:
            bool: True if the program was executed successfully, False otherwise
    '''

    ret = False
    
    # Exported the printing of the menu to a separate function.
    # This would increase the readability of the code a lot if the menu 
    # would get bigger.
    print_menu()  
       
    option: int = input('Enter an option: ')
    Option = Choice( option )
    
    if option == '1':
        ret = Option.option_1()
    elif option == '2':
        ret = Option.option_2()
    elif option == '3':
        ret = Option.option_3()
    elif option == '4':
        ret = Option.option_4()
    elif option == '5':
        ret = Option.option_5()
        
    return ret
       

if __name__ == "__main__":
    ret = set_option()
    exit( 0 if ret else 1 )
