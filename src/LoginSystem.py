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
            
        The program uses a database to store the user credentials.
        The passwords in the database are hashed using the SHA-512 algorithm to prevent
        them from being stolen in cleartext in case the database is compromised.
        
        Features in development:
            + Changing the password of an existing user
            + Deleting an existing user
            + Adding a table to the database to store the user's privileges
                + This will allow the program to support multiple users with different privileges
            
        
'''

import hashlib
import getpass as gp
import os
import sqlite3 as s

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

def db_connect():
    '''
        Description:
            Connects to the database and returns the connection and cursor objects.
        Parameters:
            None
        Returns:
            conn <sqlite3.Connection>: Connection object
            cursor <sqlite3.Cursor>: Cursor object
    '''
    
    db_name = "users.db"
    conn = s.connect(db_name)
    cursor = conn.cursor()
    
    return conn, cursor

def login( password: str, username: str) -> bool:
    '''
        Description:
            Checks if the username and password are correct.
        Parameters:
            password <str>: Password
            username <str>: Username
        Returns:
            True if the username and password are correct, False otherwise
    '''
    
    passwd_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
    
    conn, cursor = db_connect()
    value = (username,)
    sql_query = "SELECT * FROM user_credentials WHERE username = ?"
    cursor.execute(sql_query, value)
    result = cursor.fetchone()
    conn.close()
    
    if not result or result[2] != passwd_hash:
        return False    
    return True

def check_db_for_user(username: str) -> bool:
    conn, cursor = db_connect()
    value = (username,)
    sql_query = "SELECT * FROM user_credentials WHERE username = ?"
    cursor.execute(sql_query, value)
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False
    return True

def register(username: str, password: str):
    '''
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
    
    '''
    
    conn, cursor = db_connect()
    
    if check_db_for_user(username):
        return False, False
    
    try:
        passwd_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
        value = (username, passwd_hash)
        sql_query = "INSERT INTO user_credentials (username, pw_hash) VALUES (?, ?)"
        cursor.execute(sql_query, value)
        conn.commit()
        conn.close()
        
        return True, True
    except Exception as e:
        print(e)
        return False, True

def parse_args():
    '''
        Description:
            Parses the command line arguments.
        Parameters:
            None
        Returns:
            args <argparse.Namespace>: Namespace object containing the arguments
    '''
    
    # parser = argparse.ArgumentParser(description = 'Description', usage=argparse.SUPPRESS,
    #             formatter_class=lambda prog: argparse.HelpFormatter(
    #                 prog, max_help_position=80, width=120))
    
    # parser.usage = 'python3 %(prog)s [options]'
    
    # parser.add_argument('-r', '--register', action='store_true', default=False, help='Register a new user')
    
    # args = parser.parse_args()
    
    # return args
    
    return None

#
# *********** Option functions ***********
#

def option1():
    ret = False
    clear_screen()
    print('Login')
    username = input('Username: ')
    password = gp.getpass('Password: ')
    
    if not login( password, username ):
        print('Login failed!')
        ret = False
    elif login:
        print('Login successful!')
        ret = True
    return ret
    
def option2():
    clear_screen()
    print('Register a new user')
    
    username = input('Username: ') 
    password = gp.getpass('Password: ')
    password_re = gp.getpass('Repeat password: ')
    if password == password_re:
        val1, val2 = register( username, password ) 
        responses = {
            (True, True): 'User registered successfully!',
            (False, True): 'Error while registering user!',
            (True, False): 'User registered successfully, but error while creating user directory!',
            (False, False): 'Username already exists!'
        }
        print(responses[(val1, val2)])
        
        ret = True if val1 and val2 else False
    else:
        print('Passwords do not match!')
        ret = False
    return ret

def option3():
    print('Thank you for using the login system. Goodbye!')
    ret = True
    return ret

#
# ****************************************
#            

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
        '   3. Exit'
    ]
    for line in menu_string_lst:
        print(line)

def main() -> bool:
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
    print_menu()
    
    option: int = input('Enter an option: ')

    if option == '1': option1()
    elif option == '2': ret = option2()
    elif option == '3': ret = option3()

    return ret

if __name__ == "__main__":
    args = parse_args()
    
    exit( main() )

  