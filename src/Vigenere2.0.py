import getpass
import logging
from polyAlpha import Alphabet

class Logger:
    def __init__( self ):
        self.logger = logging.getLogger( __name__ )
        self.logger.setLevel( logging.DEBUG )

        console_handler = logging.StreamHandler( )
        console_handler.setLevel( logging.INFO )
        self.formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
        console_handler.setFormatter( self.formatter )
        self.logger.addHandler( console_handler )

        file_handler = logging.FileHandler( '../log/alphabet.log' )
        file_handler.setLevel( logging.DEBUG )
        file_handler.setFormatter( self.formatter )
        self.logger.addHandler( file_handler )

    def info( self, message: str ):
        self.logger.info( message )

    def debug( self, message: str ):
        self.logger.debug( message )

    def warning( self, message: str ):
        self.logger.warning( message )

    def error( self, message: str ):
        self.logger.error( message )

    def critical( self, message: str ):
        self.logger.critical( message )

def poly_vigenere_encrypt(plaintext, key, alphabets):
    ciphertext = ""
    key_index = 0
    for char in plaintext:
        if char.upper() in alphabets[key[key_index % len(key)]]:
            key_char = key[key_index % len(key)]
            char_index = alphabets[key_char].find(char.upper())
            ciphertext += alphabets[key_char][(char_index + 1) % len(alphabets[key_char])]
        else:
            ciphertext += char
        key_index += 1
    return ciphertext

def poly_vigenere_decrypt(ciphertext, key, alphabets):
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        char_index = alphabets[key[key_index % len(key)]].find(char)
        if char_index != -1:
            plaintext += alphabets[key[key_index % len(key)]][alphabets[key[key_index % len(key)]].find(char) - 1]
        else:
            plaintext += char
        key_index += 1
    return plaintext

def main( alpha_set: str, mode: str, message: str, key: str, log: Logger ) -> None:
    main_string_dict = {
        'save_file': '../data/alphabets.txt',
        'log_success': f'Successfully loaded custom alphabet set from {alpha_file}',
        'invalid_alpha_set': f'Invalid alphabet set: {alpha_set} (must be \'d\' or \'c\')',
        'entered_message': f'Entered message: {message}',
        'invalid_mode': f'Invalid mode: {mode} (must be \'e\' or \'d\')'
    }
    
    if alpha_set == 'd':
        abc = Alphabet( key )
        alphabets = abc.polyalphabet
    elif alpha_set == 'c':
        alpha_file = main_string_dict['save_file'] # string replaced for readability
        alphabets: dict[str, str] = { }
        
        with open( alpha_file, 'r') as inp:
            for line in inp:
                line = line.strip()
                key, value = line.split( ':' )
                alphabets[ key ] = value
                
        log.info( main_string_dict['log_success'] ) # string replaced for readability
    else:
        log.warning( main_string_dict['invalid_alpha_set'] ) # string replaced for readability
        exit( 1 )
    
    if mode == 'e':
        print( main_string_dict['entered_message'] )  # string replaced for readability
        print("Encrypted message: ", poly_vigenere_encrypt(message, key, alphabets))
    elif mode == 'd':
        print( main_string_dict['entered_message'] ) # string replaced for readability
        print("Decrypted message: ", poly_vigenere_decrypt(message, key, alphabets))
    else:
        print( main_string_dict['invalid_mode'] ) # string replaced for readability
        exit( 1 )
    
    return 0

if __name__ == '__main__':
    log = Logger( )
    menu_text = {
        'alpha_set': 'Do you wanna use the default alphabet set or use a custom one? (d/c) > ',
        'mode': 'Enter \'e\' for encrypt or \'d\' for decrypt: ',
        'message': 'Enter message: ',
        'example_key': 'Example key: \'ABCFTGJ\'',
        'key': 'Enter key: '
    }
    
    alpha_set = input( menu_text['alpha_set'] ).lower()
    mode = input( menu_text['mode'] ).lower()
    message = input( menu_text['message'] ).upper()
    print( menu_text['example_key'] )
    key = getpass.getpass( menu_text['key'] ).upper()
    
    ret = main(alpha_set, mode, message, key, log)
    exit( ret )
    