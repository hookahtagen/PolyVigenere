
class Alphabet:
    alphabets = {
        'A': 'EKMFLGDQVZNWOTYHXUSPIBARCJ',
        'B': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
        'C': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
        'D': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
        'E': 'VZBRGITYUPSDNHLXAWMJQOFECK',
        'F': 'JPGVOUMFYQEBNHZRDKASXLICTW',
        'G': 'NZJHGRCXMYSWBOUFAIVLPEKQDT',
        'H': 'FKQHTLXOCBJSPDZRMAEWNIUYGV',
    }
    
    def __init__( self, key: str ) -> None:
        self.key = key
        self.polyalphabet = self.getAlpha( self.key )
        
    def getAlpha( self, key: str ) -> dict[ str, str ]:
        alphabets: dict[ str, str ] = { }
        
        # For every char in the key append the corresponding dict enty
        # to the variable 'alphabets'
        
        for char in key:
            alphabets[char] = self.alphabets[char]
        
        return alphabets
    
