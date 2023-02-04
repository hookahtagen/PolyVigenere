import getpass
from polyAlpha import Alphabet


def poly_vigenere_encrypt(plaintext, key, alphabets):
    ciphertext = ""
    key_index = 0
    for char in plaintext:
        if char.upper() in alphabets[key[key_index % len(key)]]:
            char_index = alphabets[key[key_index % len(key)]].find(char.upper())
            ciphertext += alphabets[key[key_index % len(key)]][(char_index + 1) % len(alphabets[key[key_index % len(key)]])]
        else:
            ciphertext += char
        key_index += 1
    return ciphertext

def poly_vigenere_decrypt(ciphertext, key, alphabets):
    plaintext = ""
    key_index = 0
    for char in ciphertext:
        if char in alphabets[key[key_index % len(key)]]:
            plaintext += alphabets[key[key_index % len(key)]][alphabets[key[key_index % len(key)]].find(char) - 1]
        else:
            plaintext += char
        key_index += 1
    return plaintext

def main( mode: str, message: str, key: str ) -> None:
    abc = Alphabet( key )
    alphabets = abc.polyalphabet
    
    if mode == 'e':
        print(f'Entered message: {message}')
        print("Encrypted message: ", poly_vigenere_encrypt(message, key, alphabets))
    elif mode == 'd':
        print(f'Entered message: {message}')
        print("Decrypted message: ", poly_vigenere_decrypt(message, key, alphabets))
    else:
        print(f'Invalid mode: {mode} (must be \'e\' or \'d\'')
    pass

if __name__ == '__main__':
    
    mode = input("Enter \'e' for encrypt or \'d' for decrypt: ").lower()
    message = input("Enter message: ")
    key = getpass.getpass("Enter key: ").upper()
    
    main(mode, message, key)
    