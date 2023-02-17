import datetime
import hashlib
import getpass as gp
import os
import sqlite3 as s

from Vigenere import Machine

#
# ***** Defines *****
#

p_print = print

class mainProgram:
    def __init__(self, login: str) -> None:
        self.login = login
        self.machine = Machine()

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

        self.db_name = "/home/hendrik/Documents/Github/PolyVigenere/database/users.db"
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

    def print_main_menu(self):
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
        key_hash = cursor.execute(sql_query, values).fetchone()[0]
        key = gp.getpass('Enter the key to verify the connection: ')
        if hashlib.sha256(key.encode()).hexdigest() != key_hash:
            print('Wrong key! Connection not verified!')
            ret = False
            return ret
        message = input('Enter the message you want to send: ')

        verify_send_start = '''***** Below is the message you want to send *****'''
        print(verify_send_start + '\n')
        print('Message: ' + message + '\n')

        check_send: bool = input(
            'Do you want to send the message? (y/n): ') in ['y', 'Y', 'yes', 'Yes', 'YES']

        if not check_send:
            print('Message not sent!')
            print('Press enter to continue...')
            input()

            conn.close()

            ret = False
        elif check_send:
            self.clear_screen()
            print('Sending message...')
            time_stamp = str(datetime.datetime.now())

            # Encrypt the message using the key

            enciphered_message, mic = self.machine.process_message(
                'e', key, message, False, None)

            # Store the encrypted message in the database
            values = (self.login, recipient, time_stamp, enciphered_message, 0)
            sql_query = 'INSERT INTO messages (sender, recipient, timestamp, message, read) VALUES (?, ?, ?, ?, ?)'
            cursor.execute(sql_query, values)
            conn.commit()
            conn.close()

            print('Message sent!')
            print('Press enter to continue...')
            input()

            ret = True

    def option_2(self):
        ret = False
        conn, cursor = self.db_connect()

        self.clear_screen()

        # Get all messages from the database for the login
        value = (self.login, )
        sql_query = 'SELECT * FROM messages WHERE recipient = ?'

        # Store the messages in a dictionary with the timestamp as a key and a tupley as the value
        # The tuples values are: 1. the sender of the message, 2. the message itself

        # The corresponding table looks as follows:
        #   - id        INTEGER, NOT NULL, PRIMARY KEY
        #   - sender	TEXT NOT NULL,
        #   - recipient	TEXT NOT NULL,
        #   - timestamp	TEXT NOT NULL,
        #   - message	TEXT NOT NULL,
        #   - read	    INTEGER NOT NULL,

        messages = cursor.execute(sql_query, value).fetchall()
        messages_dict = {}

        for message in messages:
            messages_dict[message[3]] = (message[1], message[4])

        # Print the messages
        print('********** Messages **********')
        print('')

        # If there are no messages, print a message and return
        if not messages_dict:
            print('No messages!')
            print('Press enter to continue...')
            input()
            ret = False
        elif messages_dict:
            for timestamp, message in messages_dict.items():
                sender = message[0]
                values = (self.login, sender, sender, self.login)
                sql_query = 'SELECT alphabets FROM alpha_set WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)'

                key_hash = cursor.execute(sql_query, values).fetchone()[0]
                key = gp.getpass('Enter the key to verify the connection: ')
                if hashlib.sha256(key.encode()).hexdigest() != key_hash:
                    print('Wrong key! Connection not verified!')
                    ret = False
                    return ret

                # Decrypt the message
                deciphered_message, mic = self.machine.process_message(
                    'd', key, message[1], False, None)

                # Print the message
                print('Timestamp: ' + timestamp)
                print('Sender: ' + sender)
                print('Message: ' + deciphered_message)
                print('')

            # Mark the messages as read
            for timestamp in messages_dict.keys():
                values = (1, self.login, timestamp)
                sql_query = 'UPDATE messages SET read = ? WHERE recipient = ? AND timestamp = ?'
                cursor.execute(sql_query, values)
                conn.commit()

            print('Press enter to continue...')
            input()

            conn.close()

            ret = True

        return ret
    
    def option_3_helper(self, old_key, new_key, user_1, user_2):
        '''
            Description:
                This function provides the change of the key used for the encryption and decryption of the messages.
                It basically applies the new key to all messages that were encrypted with the old key.
            Parameters:
                self: The object itself
            Returns:
                None
        '''
        conn, cursor = self.db_connect()
        
        # The messages dict has an auto incremented integer as a key and the whole row for one message as a value
        try:
            messages = {}
            values = (user_1, user_2, user_2, user_1)
            sql_query = 'SELECT * FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)'
            result = cursor.execute(sql_query, values).fetchall()
            for message in result:
                messages[message[0]] = message

            # Apply the new key to the messages
            for id, message in messages.items():
                message = message[4]
                message, mic = self.machine.process_message('d', old_key, message, False, None)
                message, mic = self.machine.process_message('e', new_key, message, False, None)

                values = (message, id)
                sql_query = 'UPDATE messages SET message = ? WHERE id = ?'
                cursor.execute(sql_query, values)    
            val = True
        except Exception as e:
            print(e)
            val = False
        
        if val:
            conn.commit()
            
            p_message = 'The key has been changed successfully!'
            p_print(p_message)
        
        conn.close()
        

    def option_3(self):
        ret = False
        conn, cursor = self.db_connect()

        message = "Enter the username of the user you want to change the alphabet set with: "
        recipient = input(message)
        
        message = "Enter the old key: "
        old_key = input(message).upper()
        
        message = "Enter the old key again: "
        old_key_re = input(message).upper()
        
        if old_key != old_key_re:
            print('The keys do not match!')
            
            ret = False
            return ret
        elif old_key == old_key_re:
            old_key_hash = hashlib.sha256(old_key.encode()).hexdigest()
            value = (old_key_hash, )
            sql_query = 'SELECT * FROM alpha_set WHERE alphabets = ?'
            result = cursor.execute(sql_query, value).fetchone()

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

            values = (self.login, recipient, recipient, self.login)
            sql_query = 'SELECT alphabets FROM alpha_set WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)'
            
            result = cursor.execute(sql_query, values).fetchone()
            if not result:
                sql_query = 'INSERT INTO alpha_set (user_1, user_2, alphabets) VALUES (?, ?, ?)'
                key_hash: str = hashlib.sha256(key.encode()).hexdigest()
                values = (self.login, recipient, key_hash)
                cursor.execute(sql_query, values)

                print('Key created!')
                ret = True

            else:
                key_hash = hashlib.sha256(key.encode()).hexdigest()
                sql_query = 'UPDATE alpha_set SET alphabets = ? WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)'
                values = (key_hash, self.login, recipient, recipient, self.login)
                cursor.execute(sql_query, values)

                print('Key updated!')
                ret = True

            print('Press enter to continue...')
            input()

            conn.commit()
            conn.close()
            
            message = "Do you want to apply the new key to all messages that were encrypted with the old key? (y/n): "
            answer: bool = input(message).lower() == 'y'
            
            if answer:
                self.option_3_helper(old_key, key, self.login, recipient)
                

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
