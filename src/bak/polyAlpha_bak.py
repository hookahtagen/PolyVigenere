import json
import os
import random as rnd
import string
import logging
import pprint

class Logger:
    def __init__( self ):
        self.logger = logging.getLogger( __name__ )
        self.logger.setLevel( logging.DEBUG )

        console_handler = logging.StreamHandler( )
        console_handler.setLevel( logging.INFO )
        self.formatter = logging.Formatter( '%(asctime)s - %(name)s - %(levelname)s - %(message)s' )
        console_handler.setFormatter( self.formatter )
        self.logger.addHandler( console_handler )

        file_handler = logging.FileHandler( '/home/hendrik/Documents/Github/PolyVigenere/log/alphabet.log' )
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
        

class Alphabet:
    
    alphabets = {'Alpha_I': 'GAVHRIEJSWFYNQPTUDCMZKXLBO', 'Alpha_II': 'XCAJWYUGQMLHPVZKTFREOSBNDI', 'Alpha_III': 'OUIEZGFSHMKCBLYTPANVRWDJXQ', 'Alpha_IV': 'EAIFXRSPCNTUVHGDBYQMJKZWOL', 'Alpha_V': 'HTWBZJFRNYXOVUQCDPIAESGKLM', 'Alpha_VI': 'OKRXZLPSQHNJUMBTIYDWEVFGCA', 'Alpha_VII': 'CGRDETNAMUZIXQSPFKOYJLBHWV', 'Alpha_VIII': 'BCKJRULFOHADSWMYXZVTQGPENI', 'Alpha_IX': 'UNOIWSLRFMYVDGBEHZQJXCAPKT', 'Alpha_X': 'NTEGWCXHIRQZDFOJLAKYBMSPUV'}

    def __init__( self, key: str ) -> None:
        self.key = key 
        if self.key != '0': 
            self.polyalphabet = self.getAlpha( self.key )
        
    def getAlpha( self, key: str ) -> dict[ str, str ]:
        alphabets: dict[ str, str ] = { }
        
        # For every char in the key append the corresponding dict entry
        # to the variable 'alphabets'
        
        for char in key:
            alphabets[ char ] = self.alphabets[ char ]
        
        return alphabets
    
    def generate_alphabet( self, abc_count = 4 ):
        abc = ''
        abc_dict = { }
        
        def getRoman( number ):
            num = [ 1, 4, 5, 9, 10, 40, 50, 90,
                   100, 400, 500, 900, 1000 ]
            sym = [ "I", "IV", "V", "IX", "X", "XL",
                   "L", "XC", "C", "CD", "D", "CM", "M" ]
            i = 12
            roman_number = ''
      
            while number:
                div = number // num[ i ]
                number %= num[ i ]
  
                while div:
                    roman_number += sym[ i ]
                    #;print(sym[i], end = " ")
                    #print('\n')
                    div -= 1
                i -= 1
        
            return roman_number
        
        for i in range( abc_count ):
            abc = list( string.ascii_uppercase )
            rnd.shuffle(abc)
            roman_num = getRoman( i + 1 )
            abc_dict[ f'Alpha_{ roman_num }' ] = ''.join( abc )
        
        return abc_dict
    
    def save_alpha( self, abc_dict: dict[ str, str ], log: Logger ):
        ret: int = 1
        file_name = '/home/hendrik/Documents/Github/PolyVigenere/src/polyAlpha.py'
        bak_file = '/home/hendrik/Documents/Github/PolyVigenere/src/bak/polyAlpha_bak.py'
        
        try:
            with open( file_name, 'r' ) as in_file:
                buffer = in_file.readlines( )
                p_print = pprint.PrettyPrinter( indent = 4 )
                p_print.pprint( buffer )
                
                with open( bak_file, 'w' ) as bak_file:
                    bak_file.writelines( buffer )
                    log.info( 'Backup file created' )
                
                if 'class Alphabet:' in [x.strip() for x in buffer]:
                    buff_down_limit = [x.strip() for x in buffer].index('class Alphabet:')+2
                    buff_up_limit = buff_down_limit + len( abc_dict ) + 2
                else:
                    raise ValueError("Error: string 'class Alphabet:' and/or 'def __init__' not found in the list")
                
                buff_1 = buffer[ : buff_down_limit ]
                buff_2 = buffer[ buff_up_limit : ]
                
                buffer = buff_1 + [ f'    alphabets = { abc_dict }\n' ] + buff_2
                
            
                with open( file_name, 'w' ) as out_file:
                    out_file.writelines( buffer )
                    
                    
                log.info( 'Successfully saved the generated alphabets to the program.' )
                ret = 0
        except Exception as e:
            log.error( f'Error while saving the generated alphabets: { e }' )
            ret = 1
        
        return ret
        
        
    
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    
def main( log: Logger ) -> None:
    abc = Alphabet( '0' )
    alpha = { }
    
    abc_count = int( input( 'How many alphabets do you want to generate? > ' ) )
    alpha = abc.generate_alphabet( abc_count )
    
    print( 'Below you\'ll find the generated alphabets:\n' )
    p_print = pprint.PrettyPrinter( indent = 4 )
    p_print.pprint( alpha )
    save_alpha = input( '\n\nDo you want to save the generated alphabets to the program? (y/n) > ' ).lower( )
    
    ret = 1
    if save_alpha == 'y':
        ret = abc.save_alpha( alpha, log )
    elif save_alpha == 'n':
        print( 'Alphabets not saved!' )
        ret = 1
    else:
        print( 'Invalid input!' )
        ret = 1

    exit( ret )
    
    
    pass

if __name__ == '__main__':
    log = Logger( )
    
    main( log )