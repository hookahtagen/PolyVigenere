import datetime
import hashlib
import getpass as gp
import os
from re import T
import sqlite3 as s

from Vigenere import Machine
from polyAlpha import Alphabet

class mainProgram:
    def __init__(self, login: str) -> None:
        self.login = login
        
        self.print_main_menu()
        
    def db_connect(self):
        '''
            Description:
                Connects to the database and returns the connection and cursor objects.
            Parameters:
                None
            Returns:
                conn <sqlite3.Connection>: Connection object
                cursor <sqlite3.Cursor>: Cursor object
        '''
        
        self.db_name = "../database/users.db"
        self.conn = s.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
        return self.conn, self.cursor
        
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
            'Welcome, ' + self.login + '!',
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
        ret = False

        self.clear_screen()
        conn, cursor = self.db_connect()
        
        recipient = input('Enter the username of the recipient: ')
        
        # Get the alphabet set for the connection -> login - recipient from the database users.db
        #
        # The alphabet set / key is stored in the table alpha_set
        # Table alpha_set:
        #   - id: INTEGER, PRIMARY KEY, NOT NULL
        #   - user_1: TEXT, NOT NULL
        #   - user_2: TEXT, NOT NULL
        #   - alphabets: TEXT, NOT NULL
        
        values = (self.login, recipient)
        sql_query = 'SELECT alphabets FROM alpha_set WHERE user_1 = ? AND user_2 = ?'
        key = cursor.execute(sql_query, values).fetchone()[0]
        message = input('Enter the message you want to send: ')
        
        verify_send_start = '''***** Below is the message you want to send *****'''
        print(verify_send_start + '\n')
        print('Message: ' + message + '\n')
        
        check_send: bool = input('Do you want to send the message? (y/n): ') in ['y', 'Y', 'yes', 'Yes', 'YES']
        
        if not check_send:
            print('Message not sent!')
            print('Press enter to continue...')
            input()
            
            ret = False
        elif check_send:
            self.clear_screen()
            print('Sending message...')
            time_stamp = str(datetime.datetime.now())
            
            # Encrypt the message using the key
            self.alpha = Alphabet( key )
            self.alphabets = self.alpha.polyalphabet
                    
            enciphered_message = Machine.poly_vigenere_encrypt(message, key, self.alphabets) 
            
            # Store the encrypted message in the database
            values = (self.login, recipient, time_stamp, enciphered_message)
            sql_query = 'INSERT INTO messages (sender, recipient, message) VALUES (?, ?, ?)'
            cursor.execute(sql_query, values)
            conn.commit()
            
            print('Message sent!')
            print('Press enter to continue...')
            input()
            
            ret = True
    
    def option_2(self):
        pass

    def option_3(self):
        ret = False
        conn, cursor = self.db_connect()
        
        message = "Enter the username of the user you want to change the alphabet set with: "
        recipient = input(message)
        
        message = "Enter the new key: "
        key = input(message).upper()
             
        # Check if the key is valid
        #   -> Currently only the letters from A to Z are supported
        # Possible options for the key are stored in variable self.alpha.alphabets
            
        for char in key:
            if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                print('Invalid key!')
                print('Press enter to continue...')
                input()
                
                ret = False
                break
        else:
            # Update the key in the database
            sql_query = 'UPDATE alpha_set SET alphabets = ? WHERE user_1 = ? AND user_2 = ?'
            values = (key, self.login, recipient)
            cursor.execute(sql_query, values)
            conn.commit()
            
            print('Key updated!')
            print('Press enter to continue...')
            input()
            
            ret = True
        
        return ret
    
    def option_4(self):
        ret = False
        
        print('Logging out...')
        print('Press enter to continue...')
        input()
        ret = True
        
        self.clear_screen()
        return ret
    
    def option_5(self):
        ret = True
        
        print('Thank you for using my message system!')
        print('Have a nice day :)')
        
        return ret 