import hashlib
import getpass as gp
import os
import sqlite3 as sql
from types import SimpleNamespace


class Choice:
    def __init__(self, option: str, cfg: SimpleNamespace):
        self.option = option
        self.user = ''
        self.pw = ''
        self.db_file = cfg.db_file

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

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
        conn = sql.connect(self.db_file)
        cursor = conn.cursor()

        return conn, cursor

    def check_db_for_user(self, username: str) -> bool:
        conn, cursor = self.db_connect()
        value = (username,)
        sql_query = "SELECT * FROM user_credentials WHERE username = ?"
        cursor.execute(sql_query, value)
        result = cursor.fetchone()
        conn.close()

        if not result:
            return False
        return True

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

    def login_helper(self, password: str, username: str) -> tuple[bool, str]:
        """
            Description:
                Checks if the username and password are correct.
            Parameters:
                password <str>: Password
                username <str>: Username
            Returns:
                True if the username and password are correct, False otherwise
        """

        passwd_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()

        result = self.sql_queries(
            'SELECT',
            'SELECT * FROM user_credentials WHERE username = ?',
            (username,),
            fetch='one'
        )

        if not result or result[2] != passwd_hash:
            return False, 'None'
        return True, result[1]

    def register(self, username: str, password: str):
        """
            Description:
                Registers a new user.
            Parameters:
                username <str>: Username
                password <str>: Password
            Returns:
                False, False if the username already exists
                False, True if there was an error while registering the user
                True, False if there was an error while creating the user directory
                True, True if the user was registered successfully

        """

        if self.check_db_for_user(username):
            return False, False

        try:
            passwd_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()

            _ = self.sql_queries(
                'INSERT',
                'INSERT INTO user_credentials (username, pw_hash) VALUES (?, ?)',
                (username, passwd_hash),
                fetch='None'
            )

            return True, True
        except Exception as e:
            print(e)
            return False, True

    @staticmethod
    def check_pw(self, mode: str, key_word='') -> str:
        """
            Description:
                Checks if the two passwords are the same.
            Parameters:
                passwd1 <str>: Password 1
                passwd2 <str>: Password 2
                mode <str>: Mode of operation
            Returns:
                True if the passwords are the same, False otherwise
        """
        str_1 = str_2 = ''
        if mode == 'register':
            pass
        elif mode == 'change':
            str_1 = f'Enter {key_word} password: '
            str_2 = f'Repeat {key_word} password: '
        elif mode == 'delete':
            str_1 = 'Enter password: '
            str_2 = 'Repeat password: '

        passwd = gp.getpass(str_1)
        passwd_re = gp.getpass(str_2)

        if passwd != passwd_re:
            print('Passwords do not match!')
            exit(1)

        return passwd

    def login(self):
        ret = False
        self.clear_screen()
        print('Login')
        username = input('Username: ')
        password = gp.getpass('Password: ')

        val, login = self.login_helper(password, username)
        if not val:
            print('Login failed!')
            ret = False
        elif val:
            print('Login successful!')
            self.user = username
            self.pw = password
            ret = True

        return ret

    def register_new_user(self):
        self.clear_screen()
        print('Register a new user')

        username = input('Username: ')

        password = gp.getpass('Password: ')
        password_re = gp.getpass('Repeat password: ')

        if password == password_re:
            val1, val2 = self.register(username, password)
            responses = {
                (True, True): 'User registered successfully!',
                (False, True): 'Error while registering user!',
                (True, False): 'User registered successfully, but error while creating user directory!',
                (False, False): 'Username already exists!'
            }
            print(responses[(val1, val2)])

            ret = True if val1 and val2 else False
            self.user = username if val1 and val2 else ''
            self.pw = password if val1 and val2 else ''
        else:
            print('Passwords do not match!')
            ret = False

        return ret

    def change_password(self):
        """
            Description:
                Changes the password of an existing user.
            Parameters:
                None
            Returns:
                True if the password was changed successfully, False otherwise
        """

        ret = False
        value_1 = [None, None]  # username, pw_hash
        value_2 = [None, None]  # pw_hash, username

        value_1[0] = value_2[1] = input(
            'Type in the username of the user whose password you want to change: ')
        passwd = self.check_pw("change", "current")
        value_1[1] = hashlib.sha512(passwd.encode('utf-8')).hexdigest()

        result = self.sql_queries(
            'SELECT',
            'SELECT * FROM user_credentials WHERE username = ? AND pw_hash = ?',
            (value_1[0], value_1[1]),
            fetch='one'
        )

        # Check if the passwords in result and passwd match
        if not result:
            print('Username or password incorrect!')
            ret = False

            return ret

        print("\n")
        new_passwd = self.check_pw("change", "new")
        value_2[0] = hashlib.sha512(new_passwd.encode('utf-8')).hexdigest()

        result = self.sql_queries(
            'UPDATE',
            'UPDATE user_credentials SET pw_hash = ? WHERE username = ?',
            (value_2[0], value_2[1]),
            fetch='None'
        )

        message = 'Password changed successfully!' if result else 'Error while changing password!'
        print(message)

        self.user = value_1[0] if result else ''
        self.pw = new_passwd if result else ''
        ret = True if result else False
        return ret

    def delete_account(self):
        """
            Description:
                Deletes an existing user from the database.
            Parameters:
                None
            Returns:
                True if the user was deleted successfully, False otherwise
        """
        ret = False
        str_lst = [
            'Type in the username of the user you want to delete: ',
            'User deleted successfully!',
            'Error while deleting user!'

        ]
        query_lst = [
            "SELECT * FROM user_credentials WHERE username = ? AND pw_hash = ?",
            "DELETE FROM user_credentials WHERE username = ?"
        ]

        username = input(str_lst[0])
        passwd = self.check_pw('delete', '')
        passwd_hash = hashlib.sha512(passwd.encode('utf-8')).hexdigest()
        stored_passwd = self.sql_queries(
            'SELECT',
            query_lst[0],
            values=(
                username,
                passwd_hash
            ),
            fetch='one'
        )

        if not stored_passwd or stored_passwd[1] != passwd_hash:
            print('Username or password incorrect!')
            ret = False

            return ret

        result = self.sql_queries(
            'DELETE',
            query_lst[1],
            values=(
                username,

            ),
            fetch='None'
        )

        val = self.sql_queries(
            'SELECT',
            'SELECT * FROM user_credentials WHERE username = ?',
            (username,),
            fetch='one'
        )

        if not val or result:
            print(str_lst[1])
            ret = True

        elif val and not result:
            print(str_lst[2])
            ret = False

        return ret

    @staticmethod
    def setup_exit(self):
        print('Thank you for using my message system! :)')
        print('Goodbye!')
        ret = True

        return ret
