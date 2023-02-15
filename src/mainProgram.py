import hashlib
import getpass as gp
import os
from re import T
import sqlite3 as s

class mainProgram:
    def __init__(self, option: str) -> None:
        self.option = option
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
            
    def option_1(self):
        self.clear_screen()
        
        recipient = input('Enter the username of the recipient: ')
        message = input('Enter the message you want to send: ')
        
        check_send: bool = input('Do you want to send the message? (y/n): ') == 'y'
    
    def option_2(self):
        pass

    def option_3(self):
        pass
    
    def option_4(self):
        self.option_5()
    
    def option_5(self):
        ret = True
        
        print('Thank you for using my message system!')
        print('Have a nice day :)')
        
        return ret 