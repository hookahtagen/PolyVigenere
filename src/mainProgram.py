import datetime
import hashlib
import getpass as gp
import os
import sqlite3 as s
from types import SimpleNamespace

from Vigenere import Machine


class mainProgram:
    def __init__(self, login: str, cfg: SimpleNamespace) -> None:
        self.login = login
        self.machine = Machine()
        self.cfg = cfg

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

        self.db_name = os.path.join(self.cfg.db_path, self.cfg.db_name)
        self.conn = s.connect(self.db_name)
        self.cursor = self.conn.cursor()

        return self.conn, self.cursor

    def sql_queries(self, keyword: str, query: str, values: tuple, fetch: str = 'all'):
        '''
            Description:
                Executes a SQL query. The query is executed based on the keyword.
                The keyword is used to determine which function should be executed.

                The fetch parameter is used to determine if the query should return
                all the results or just one. If the fetch parameter is not specified
                or set to 'None', the query will not return anything.
            Parameters:
                query <str>: SQL query
                values <tuple>: Values to be inserted into the query
            Returns:
                result: The result of the query. If the query is an INSERT, UPDATE or SELECT
        '''
        result = None

        def INSERT(conn, cursor):
            cursor.execute(query, values)
            conn.commit()
            result = True

            return result

        def SELECT(conn, cursor):
            cursor.execute(query, values)
            fetch_lst = [cursor.fetchall(), cursor.fetchone()]
            result = fetch_lst[0] if fetch == 'all' else fetch_lst[1]

            return result

        def UPDATE(conn, cursor):
            '''
                For now this function is the same as INSERT.
                So therefor it's just a placeholder and 'redirects' to INSERT.
            '''
            INSERT(conn, cursor)

        def DELETE(conn, cursor):
            cursor.execute(query)
            conn.commit()
            result = True

            return result

        conn, cursor = self.db_connect()
        keyword_lst = {
            'INSERT': INSERT,
            'SELECT': SELECT,
            'UPDATE': UPDATE,
            'DELETE': DELETE
        }

        try:
            result = keyword_lst[keyword](conn, cursor)
        except Exception as e:
            print(e)
            conn.close()
            result = False

        conn.close()
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
        Welcome,{self.login}!\n
        What do you want to do?
            Messaging options:
                1. Send a message
                2. Read your unread messages
                3. Edit your alphabet set with another user
                4. Delete your account
        
            Logout/Exit:
                5. Logout
                6. Exit
        '''

        self.clear_screen()
        print(main_menu)

    def send_message(self):
        ret = False
        str_lst = [
            'Enter the username of the recipient: ',
            'Enter the key to verify the connection: ',
            'Wrong key! Connection not verified!',
            'Enter the message you want to send: ',
            'Do you want to send the message? (y/n): ',
            'Sending message...',
            'Message sent!',
            'Something went wrong while sending the message! Please try again!'
        ]
        query_lst = [
            'SELECT alphabets FROM alpha_set WHERE user_1 = ? AND user_2 = ?',
            'INSERT INTO messages (sender, recipient, timestamp, message, read) VALUES (?, ?, ?, ?, ?)'
        ]
        val_tuple = [
            'y',
            'Y',
            'yes',
            'Yes',
            'YES']

        self.clear_screen()

        recipient = input(str_lst[0])

        key = self.sql_queries(
            'SELECT',
            query_lst[0],
            (self.login, recipient),
            fetch='one'
        )[0]

        key_val = gp.getpass(str_lst[1]).upper()
        if key != key_val:
            print(str_lst[2])
            ret = False
            return ret
        message = input(str_lst[3])

        verify_send_start = f'''
        ***** Below is the message you want to send *****
        _________________________________________________
        
        Message: {message}
        
        _________________________________________________
        '''
        print(verify_send_start)

        check_send: bool = input(str_lst[4]) in val_tuple

        if not check_send:
            print('Message not sent!')
            self.p_continue()

            ret = False

        elif check_send:
            self.clear_screen()
            print(str_lst[5])
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
                query_lst[1],
                values=(
                    self.login,
                    recipient,
                    time_stamp,
                    enciphered_message,
                    0
                ),
                fetch=None
            )

            print(str_lst[6] if result else str_lst[7])
            self.p_continue()

            ret = True

        return ret

    def show_unread_messages(self):
        ret = False
        str_lst = [
            '********** Messages **********\n\n',
            'No unread messages!',
            'Something went wrong while retrieving the messages!\nPlease try again!'
        ]
        query_lst = [
            'SELECT * FROM messages WHERE recipient = ? AND read = 0',
            'SELECT * FROM messages WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)',
            'UPDATE messages SET read = ? WHERE recipient = ? AND timestamp = ?'

        ]

        self.clear_screen()

        # Get all messages from the database for the logged in user
        result = self.sql_queries(
            'SELECT',
            query_lst[0],
            values=(
                self.login,
            ),
            fetch='all'
        )

        messages_dict = {}
        for message in result:
            messages_dict[message[3]] = (message[1], message[4])

        # Print the messages. If there are no messages, print a message and return
        print(str_lst[0])
        if not messages_dict:
            print(str_lst[1])
            self.p_continue()
            ret = True
        elif messages_dict:
            for timestamp, message in messages_dict.items():
                sender = message[0]

                key_hash = self.sql_queries(
                    'SELECT',
                    query_lst[1],
                    values=(
                        self.login,
                        sender,
                        sender,
                        self.login),
                    fetch='one'
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
                    query_lst[2],
                    values=(
                        1,
                        self.login,
                        timestamp),
                    fetch=None
                )

                if not result:
                    print(str_lst[2])
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

        str_lst = [
            'The key has been changed successfully!',
            '''
            Something went wrong while changing the key!
            No messages were changed!
            Please try again!
            '''
        ]
        query_lst = [
            'SELECT * FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)',
            'UPDATE messages SET message = ? WHERE id = ?'
        ]
        # The messages dict has an auto incremented integer as a key and the whole row for one message as a value
        try:
            messages = {}

            result = self.sql_queries(
                'SELECT',
                'SELECT * FROM messages WHERE (sender = ? AND recipient = ?) OR (sender = ? AND recipient = ?)',
                values=(
                    user_1,
                    user_2,
                    user_2,
                    user_1
                ),
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
                    values=(
                        message,
                        id
                    ),
                    fetch=None
                )
            val = True
        except s.Error as e:
            print(e)
            val = False

        if val:
            print(str_lst[0])
        elif not val:
            print(str_lst[1])

    def edit_key(self):
        ret = False
        str_lst = [
            'Enter the username of the user you want to change the alphabet set with: ',
            'Enter the old key: ',
            'Wrong key!',
            'Enter the new key: ',
            'Enter the new key again: ',
            'The keys do not match!',
            'Key successfully edited!',
            'Do you want to apply the new key to all messages that were encrypted with the old key? (y/n): '
        ]
        query_lst = [
            'SELECT alphabets FROM alpha_set WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)',
            'INSERT INTO alpha_set (user_1, user_2, alphabets) VALUES (?, ?, ?)',
            'UPDATE alpha_set SET alphabets = ? WHERE (user_1 = ? AND user_2 = ?) OR (user_1 = ? AND user_2 = ?)'
        ]

        recipient = input(str_lst[0])

        old_key = gp.getpass(str_lst[1]).upper()

        result = self.sql_queries(
            'SELECT',
            query_lst[0],
            values=(
                self.login,
                recipient,
                recipient,
                self.login
            ),
            fetch='one'
        )
        if result:
            if result[0] != old_key:
                print(str_lst[2])
                self.p_continue()

                ret = False
                return ret
        elif not result:
            pass

        key = gp.getpass(str_lst[3]).upper()

        key_re = gp.getpass(str_lst[4]).upper()

        if key != key_re:
            print(str_lst[5])
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
            query_lst[0],
            values=(
                self.login,
                recipient,
                recipient,
                self.login
            ),
            fetch='one'
        )

        if not result:
            result = self.sql_queries(
                'INSERT',
                query_lst[1],
                values=(
                    self.login,
                    recipient,
                    key
                ),
                fetch=None
            )

        elif result:
            result = self.sql_queries(
                'UPDATE',
                query_lst[2],
                values=(
                    key,
                    self.login,
                    recipient,
                    recipient,
                    self.login
                ),
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
            print(str_lst[6])
            ret = True

        self.p_continue()

        answer: bool = input(str_lst[7]).lower() == 'y'

        if answer:
            self.apply_new_key(old_key, key, self.login, recipient)

        return ret

    def delete_account(self):
        ret = False
        str_lst = [
            'Enter the username of the account you want to delete: ',
            'Enter the password: ',
            'Enter the password again: ',
            'Wrong password!',
            '''
            The account has been deleted successfully!
            You will be logged out now!
            Goodbye and have a nice day :)
            '''
        ]
        query_lst = [
            'SELECT * FROM users WHERE username = ?',
            'DELETE FROM users WHERE username = ?',
        ]

        username = input(str_lst[0])

        passwd = hashlib.sha256(gp.getpass(str_lst[1]).encode()).hexdigest()
        passwd_re = hashlib.sha256(gp.getpass(str_lst[2]).encode()).hexdigest()

        stored_user_password = self.sql_queries(
            'SELECT',
            query_lst[0],
            values=(
                username,
            ),
            fetch='one'
        )

        if passwd not in [passwd_re, stored_user_password[2]]:
            print(str_lst[3])
            self.p_continue()

            ret = False
            return ret
        elif passwd in [passwd_re, stored_user_password[2]]:
            result = self.sql_queries(
                'DELETE',
                query_lst[1],
                values=(
                    username,
                ),
                fetch=None
            )

            if not result:
                print(str_lst[3])
                self.p_continue()

                ret = False
                return ret

            print(str_lst[4])
            self.p_continue()

            ret = True
            self.logout()

    def logout(self):
        ret = False
        str_lst = [
            'Logging out...'
        ]

        print(str_lst[0])
        self.p_continue()

        ret = True
        self.clear_screen()

        return ret

    def main_exit(self):
        ret = True
        str_lst = [
            '''
            Thank you for using my message system!
            Have a nice day :)
            '''
        ]

        print(str_lst[0])

        return ret
