## Polyalphabetic Cipher Encrypter/Decrypter

### Description:<br>
<hr>
This program allows for encryption and decryption of plaintext messages using a polyalphabetic cipher. The program uses an alphabet dictionary <br>
to define the different alphabets for each character in the key. The key is then used to shift the corresponding character in the plaintext <br>
by one place for encryption, or by one place in reverse for decryption. <br>
<br>
The program also allows for the use of a custom alphabet dictionary, which can be used to define the alphabets for each character in the key. <br>
The default alphabet dictionary is as follows:<br> <br>  

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

<br>
Note: In an acutal application it would be unsafe to store the alphabet dictionary in the program itself, as it would be easy for an attacker to find the <br>
mapping of key characters to alphabets. Instead, the alphabet dictionary should be stored in a separate file, and the program should be modified to read <br>
the dictionary from the file. This would wouldn't be a secure method of storing the alphabet dictionary, but it would be better than storing it in the program itself.

<br>

### Get Started:<br>
<hr>


    + Clone the repository to your local machine.

    + Navigate to the PolyVigenere/src directory.

    + Run the Vigenere2.0.py program using Python 3.


Et voila! You're ready to go! [^src]

<br>

### Usage:<br>
<hr>


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

<br>

### Example:<br>
<hr>

The following >>example<< shows the program being used to encrypt the message "therussiansarecoming" using the key "abcdefg". <br><br>

```console
hendrik@the-machine:~/Documents/Github$ /bin/python3 /home/hendrik/Documents/Github/PolyVigenere/src/Vigenere2.0.py
Enter 'e' for encrypt or 'd' for decrypt: e
Enter message: therussiansarecoming
Enter key: abcdefg (<- Is actually hidden in the terminal)
Entered message: therussiansarecoming
Encrypted message:  YWIHPXWBJYOWDKJEURHV
```

<br>
<br>

#### Planned Features:<br>
<hr>


    + Add support for enciphering/deciphering txt files.
    + Add a generator for the alphabet dictionary.
    + 

<br>
<hr>

##### Notes:<br>
<br>
src/Vigenere2.0.py
[^src]: Source Code: [Vigenere2.0.py](github.com/hookahtagen/PolyVigenere/blob/764eb8e6e3dc6f9f6863e55f012b5b28e4659def/src/Vigenere2.0.py)