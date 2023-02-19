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

    def p_continue(self):
        print('Press enter to continue...')
        input()

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

    def sql_queries(self, keyword: str, query: str, values: tuple, fetch: str = 'all'):
        '''
            Description:
                Executes a SQL query.
            Parameters:
                query <str>: SQL query
                values <tuple>: Values to be inserted into the query
            Returns:
                result <tuple>: Result of the query
        '''
        result = None
        conn, cursor = self.db_connect()

        if keyword == 'INSERT':
            try:
                cursor.execute(query, values)
                conn.commit()
                conn.close()
                result = True
            except Exception as e:
                print(e)
                conn.close()
                result = False
        elif keyword == 'SELECT':
            try:
                cursor.execute(query, values)
                if fetch == 'all':
                    result = cursor.fetchall()
                elif fetch == 'one':
                    result = cursor.fetchone()
                conn.close()
            except Exception as e:
                print(e)
                conn.close()
                result = False
        elif keyword == 'UPDATE':
            try:
                cursor.execute(query, values)
                conn.commit()
                conn.close()
                result = True
            except Exception as e:
                print(e)
                conn.close()
                result = False
        elif keyword == 'DELETE':
            pass

        del conn, cursor

        return result

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
        
        main_menu = f'''
        ********** Main Menu **********
        Welcome,{self.login}!
        What do you want to do?
            Messaging options:
                1. Send a message
                2. Read your unread messages
                3. Edit your alphabet set with another user
        
            Logout/Exit:
                4. Logout
                5. Exit
        '''

        self.clear_screen()
        print(main_menu)

    def send_message(self):
        ret = False
        self.clear_screen()

        recipient = input('Enter the username of the recipient: ')

        key = self.sql_queries(
            'SELECT'
            'SELECT alphabets FROM alpha_set WHERE user_1 = ? AND user_2 = ?',
            (self.login, recipient),
            fetch='one'
        )[0]

        key_val = gp.getpass(
            'Enter the key to verify the connection: ').upper()
        if key != key_val:
            print('Wrong key! Connection not verified!')
            ret = False
            return ret
        message = input('Enter the message you want to send: ')

        verify_send_start = '''
        ***** Below is the message you want to send *****
        _________________________________________________
        '''
        print(verify_send_start)
        print('Message: ' + message + '\n')

        check_send: bool = input(
            'Do you want to send the message? (y/n): ') in ['y', 'Y', 'yes', 'Yes', 'YES']

        if not check_send:
            print('Message not sent!')
            self.p_continue()

            ret = False

        elif check_send:
            self.clear_screen()
            print('Sending message...')
            time_stamp = str(datetime.datetime.now())

            # Encrypt the message using the key
            enciphered_message, mic = self.machine.process_message(
                'e',
                key,
                message,
                False,
                None
            )

            # Store the encrypted message in the database
            result = self.sql_queries(
                'INSERT',
                'INSERT INTO messages (sender, recipient, timestamp, message, read) VALUES (?, ?, ?, ?, ?)',
                (self.login, recipient, time_stamp, enciphered_message, 0),
                fetch=None
            )

            message = 'Message sent!' if result else 'Something went wrong while sending the message! Please try again!'
            print(message)
            self.p_continue()

            ret = True

        return ret

    def show_unread_messages(self):
        ret = False

        self.clear_screen()

        # Get all messages from the database for the logged in user
        result = self.sql_queries(
            'SELECT',
            'SELECT * FROM messages WHERE recipient = ?',
            (self.login, ),
            fetch=None
        )

        messages_dict = {}

        for message in result:
            messages_dict[message[3]] = (message[1], message[4])

        # Print the messages
        messages_header = '''
        ********** Messages **********\n
        
        '''
        print(messages_header)

        # If there are no messages, print a message and return
        if not messages_dict:
            print('No unread messages!')
            self.p_continue()
            ret = True
        elif messages_dict:
            for timestamp, message in messages_dict.items():
                sender = message[0]

                key_hash = self.sql_queries_result(
                    'SELECT alphabets FROM alpha_set WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)',
                    'self.login, sender, sender, self.login',
                    'one'
                )[0]

                # Decrypt the message
                deciphered_message, mic = self.machine.process_message(
                    'd',
                    key_hash.upper(),
                    message[1],
                    False,
                    None
                )

                # Print the message
                print('Timestamp: ' + timestamp)
                print('Sender: ' + sender)
                print('Message: ' + deciphered_message)
                print('')

            # Mark the messages as read
            for timestamp in messages_dict.keys():
                result = self.sql_queries(
                    'UPDATE',
                    'UPDATE messages SET read = ? WHERE recipient = ? AND timestamp = ?',
                    (1, self.login, timestamp),
                    fetch=None
                )

                if not result:
                    print('Something went wrong while marking the messages as read!')
                    print('Please try again!')
                    ret = False
                elif result:
                    ret = True

            self.p_continue()

        return ret

    def apply_new_key(self, old_key, new_key, user_1, user_2):
        '''
            Description:
                This function provides the change of the key used for the encryption and decryption of the messages.
                It basically applies the new key to all messages that were encrypted with the old key.
            Parameters:
                self: The object itself
            Returns:
                None
        '''

        # The messages dict has an auto incremented integer as a key and the whole row for one message as a value
        try:
            messages = {}

            result = self.sql_queries(
                'SELECT',
                'SELECT * FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)',
                (user_1, user_2, user_2, user_1),
                fetch='all'
            )
            for message in result:
                messages[message[0]] = message

            # Apply the new key to the messages
            for id, message in messages.items():
                message = message[4]
                message, mic = self.machine.process_message(
                    'd', old_key, message, False, None)
                message, mic = self.machine.process_message(
                    'e', new_key, message, False, None)

                result = self.sql_queries(
                    'UPDATE',
                    'UPDATE messages SET message = ? WHERE id = ?',
                    (message, id),
                    fetch=None
                )
            val = True
        except Exception as e:
            print(e)
            val = False

        if val:
            p_message = 'The key has been changed successfully!'
            p_print(p_message)

    def edit_key(self):
        ret = False

        message = "Enter the username of the user you want to change the alphabet set with: "
        recipient = input(message)

        message = "Enter the old key: "
        old_key = gp.getpass(message).upper()

        result = self.sql_queries(
            'SELECT',
            'SELECT alphabets FROM alpha_set WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)',
            (self.login, recipient, recipient, self.login),
            fetch='one'
        )
        if result:
            if result[0] != old_key:
                print('Wrong key!')
                self.p_continue()

                ret = False
                return ret
        elif not result:
            pass

        message = "Enter the new key: "
        key = gp.getpass(message).upper()

        message = "Enter the new key again: "
        key_re = gp.getpass(message).upper()

        if key != key_re:
            print('The keys do not match!')
            self.p_continue()

            ret = False
            return ret

        # Check if the key is valid
        #   -> Currently only the letters from A to Z are supported
        # Possible options for the key are stored in variable self.alpha.alphabets

        for char in key:
            if char not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                print('Invalid key!')
                self.p_continue()

                ret = False
                break
            else:
                pass

        result = self.sql_queries(
            'SELECT',
            'SELECT alphabets FROM alpha_set WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)',
            (self.login, recipient, recipient, self.login),
            fetch='one'
        )

        if not result:
            result = self.sql_queries(
                'INSERT',
                'INSERT INTO alpha_set (user_1, user_2, alphabets) VALUES (?, ?, ?)',
                (self.login, recipient, key),
                fetch=None
            )

        elif result:
            result = self.sql_queries(
                'UPDATE',
                'UPDATE alpha_set SET alphabets = ? WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)',
                (key, self.login, recipient, recipient, self.login),
                fetch=None
            )

        if not result:
            error_message = '''
            Something went wrong while updating the key!\n
            Please try again!
            '''
            print(error_message)
            ret = False

        elif result:
            print('Key successfully edited!')
            ret = True

        self.p_continue()

        message = "Do you want to apply the new key to all messages that were encrypted with the old key? (y/n): "
        answer: bool = input(message).lower() == 'y'

        if answer:
            self.apply_new_key(old_key, key, self.login, recipient)

        return ret

    def logout(self):
        ret = False

        print('Logging out...')
        self.p_continue()

        ret = True
        self.clear_screen()

        return ret

    def main_exit(self):
        ret = True

        exit_message = '''
        Thank you for using my message system!
        Have a nice day :)
        '''
        print(exit_message)

        return ret
