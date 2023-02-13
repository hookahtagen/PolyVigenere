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

    def print_menu( self ):
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
            'Welcome to Vigenere Secret Chat!',
            'Please choose an option:',
            '   1. Login',
            '   2. Register',
            '   3. Change password',
            '   4. Delete account',
            '   5. Exit'
        ]
        
        self.clear_screen()
        for line in menu_string_lst:
            print(line)
            
class mainProgram:
    def __init__(self):
        self.print_main_menu()
        
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
    
    def print_main_menu( self ):
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
        
        main_menu_string_lst = [
            '********** Main Menu **********',
            '',
            'What do you want to do?',
            '   1. Send a message',
            '   2. Read your messages',
            '   3. Change your alphabet set',
            '   ',
            '   4. Logout',
            '   5. Exit'
        ]
        
        self.clear_screen()
        for line in main_menu_string_lst:
            print(line)

def main( machine: System ):
    main_prog = mainProgram()
    
    pass            

def setup() -> bool:
    machine = System()
    machine.print_menu()
    
    message = 'Please choose an option: '
    option: int = input( message )
    Option = Choice( option )
    
    if option == '1':
        ret = Option.option_1()
        if ret:
            main( machine )
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
    exit( 0 if ret else 1 )
