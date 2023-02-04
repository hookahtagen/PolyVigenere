## Polyalphabetic Cipher Encrypter/Decrypter

### Description:<br>
<sup>This program allows for encryption and decryption of plaintext messages <br>
using a polyalphabetic cipher. The program uses an alphabet dictionary <br>
to define the different alphabets for each character in the key. The <br>
key is then used to shift the corresponding character in the plaintext <br>
by one place for encryption, or by one place in reverse for decryption. <br>
<br>
The program also allows for the use of a custom alphabet dictionary, <br>
which can be used to define the alphabets for each character in the key. <br>
The default alphabet dictionary is as follows:<br>  
```
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
```
</sup>

### Usage:<br>
<sup>

    + Define the alphabets dictionary with the desired mapping of key characters
    to their corresponding alphabets.

    + Specify the key to be used for encryption/decryption.

    + Call the poly_vigenere_encrypt function with the plaintext message to be
    encrypted and the key, along with the alphabets dictionary. The encrypted
    message will be returned.

    + Call the poly_vigenere_decrypt function with the encrypted message and the 
    key, along with the alphabets dictionary. The decrypted message will be returned.

    + Note: This program only works with single-character mappings of key characters to
    alphabets, and does not support multiple characters per alphabet.
</sup>
### Example:<br>
<sup>
The program also allows for the use of a custom alphabet dictionary, <br>
which can be used to define the alphabets for each character in the key. <br>
The default alphabet dictionary is as follows:<br>  
```
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
```
</sup>
