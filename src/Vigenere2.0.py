import getpass
import json
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
        
class Machine:
    def __init__( self ) -> None:
        self.initialized = "Machine Initialized"
        return None
        
    def process_message( self, mode: str, key: str, message: str, file_enc: bool, file_name: str ) -> str:
        self.mode = mode
        self.key = key
        self.message = message
        self.alphabets: dict[ str, str ] = { }
        self.file_enc = file_enc
        
        self.alpha = Alphabet( key )
        self.alphabets = self.alpha.polyalphabet
        
        if self.mode == 'e':
            self.processed_message = self.poly_vigenere_encrypt( self.message, self.key, self.alphabets )
        elif self.mode == 'd':
            self.processed_message = self.poly_vigenere_decrypt( self.message, self.key, self.alphabets )
        
        if not self.file_enc:
            return self.processed_message
        else:
            with open( file_name.replace('.txt','_enc.txt'), 'w' ) as file:
                file.write( self.processed_message )
            
            if self.mode == 'd':
                return "File decrypted successfully"
            else:
                return "File encrypted successfully"
        
    def poly_vigenere_encrypt(self, plaintext: str, key: str, alphabets: dict[str, str] ) -> str:
        '''
        Description:
            This function takes a plaintext string and a key string and encrypts the plaintext using the key.
            Every character in the plaintext is encrypted using the character in the key that corresponds to it.

        Args:
            plaintext (str): _description_
            key (str): _description_
            alphabets (dict[str, str]): _description_

        Returns:
            str: _description_
        '''    
        
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

    def poly_vigenere_decrypt(self, ciphertext: str, key: str, alphabets: dict[str, str]) -> str:
        '''
        Description:
            This function takes a ciphertext string and a key string and decrypts the ciphertext using the key.
            
        Args:
            ciphertext (str): _description_
            key (str): _description_
            alphabets (dict[str, str]): _description_

        Returns:
            str: _description_
        '''    
        
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

def main( log: Logger ) -> None:     
    ret = 1
    machine = Machine( )
    log.info( machine.initialized )
    
    print( "Welcome to the PolyVigenere Machine" )
    print( "You have either the option to use the settings file or enter the settings manually")
    settings_file: bool = True if input( "Do you want to use the settings file? (y/n): ") == 'y' else False
    
    file_enc: bool = True if input( "Do you want to encrypt or decrypt a file? (y/n): ") == 'y' else False
    mode = input( "Do you want to encrypt or decrypt a message? (e/d): " )
    if settings_file:
        in_settings: dict[ str, str ] = { }
        with open( '../data/settings.cfg', 'r' ) as in_file:
            for line in in_file:
                line = line.strip()
                a_key, value = line.split( '=' )
                in_settings[ a_key ] = value
        key = in_settings[ 'key' ].upper( )
            
    elif not settings_file:
        key = input( "Enter the key: " ).upper( )
        
    if not file_enc:
        message = input( "Enter the message: " )
        p_message = machine.process_message( mode, key, message, file_enc, None )
        log.info( f'Processed Message: {p_message}')
        
        ret = 0
    else:
        file_name = input( "Enter the file name: " )
        with open( file_name, 'r' ) as file:
            message = file.read( )
        p_message = machine.process_message( mode, key, message, file_enc, file_name )
        
        log.info( p_message )

        ret = 1 

    return ret

if __name__ == '__main__':
    log = Logger( )    
    ret = main( log )
    
    exit( ret )
    