
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
        self.key = key.upper( )
        self.alphabets = self.getAlpha( self.key )
        
    def getAlpha( self, key: str ) -> str:
        alphabets: dict[ str, str ]
        
        for char in key:
            if char in self.alphabets:
                return self.alphabets[ char ]
        
        return alphabets