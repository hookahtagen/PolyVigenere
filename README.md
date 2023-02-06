# Polyalphabetic Cipher Encrypter/Decrypter

![vignere-cipher](https://steamuserimages-a.akamaihd.net/ugc/781867089027223194/99CFD48BB59612E4F6FECD0600EBE920BED846B6/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false) [^vigenere-cipher]

## Documentation:<br>

For information on how to use the program, please refer to the [Documentation.md](/test/Documentation.md) file. <br><br>

## Description:<br>

This program allows for enciphering and deciphering of plaintext messages using a polyalphabetic cipher. The program uses an alphabet dictionary <br>
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

#### Note:
====================

In an acutal application it would be unsafe to store the alphabet dictionary in the program itself, as it would be easy for an attacker to find the <br>
mapping of key characters to alphabets. Instead, the alphabet dictionary should be stored in a separate file, and the program should be modified to read <br>
the dictionary from the file. This would wouldn't be a secure method of storing the alphabet dictionary, but it would be better than storing it in the program itself.<br><br>

## Installation:<br>

For information on how to install the program, please refer to the [Install.md](https://github.com/hookahtagen/PolyVigenere/blob/main/src/Install.md) file. <br><br>


## Get Started:<br>

    + Clone the repository to your local machine.

    + Navigate to the PolyVigenere/src directory.

    + Run the Vigenere2.0.py program using Python 3.


Et voila! You're ready to go! [^src] <br><br>


## Usage:<br>

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


## Example:<br>

### Example usage of Vigenere2.0.py:<br>

The following **example** shows the program being used to encipher the message "therussiansarecoming" using the key "abcdefg". <br><br>

```console
hendrik@example:~$ /bin/python3 /home/hendrik/Documents/Github/PolyVigenere/src/Vigenere2.0.py
Do you wanna use the default alphabet set or use a custom one? (d/c) > d
Enter 'e' for encrypt or 'd' for decrypt: e
Enter message: therussiansarecoming
Example key: 'ACBDLJ'
Enter key: ACBDLJ (<-- Is actually hidden in the terminal)
Entered message: therussiansarecoming
Encrypted message:  RVNEBEHYPMLDOYVHXYYR
```

<br>

### Example usage of the generator for the alphabet dictionary:<br>

The following **example** shows the usage of the generator for the alphabet dictionary. <br><br>

```console
hendrik@example:$ /bin/python3 /home/hendrik/Documents/Github/PolyVigenere/src/polyAlpha.py
How many alphabets do you want to generate? > 20
Below you'll find the generated alphabets:

{   'Alpha_I': 'BNKGVJIALPCFWXSRDYHUOZTMQE',
    'Alpha_II': 'THEWMXGZAKJPSORCLFQBYUDVIN',
    'Alpha_III': 'CUZHKXAPTMFQYNBJWGIVSLERDO',
    'Alpha_IV': 'SXAJZPHWFQRCBUEINDYTVMKGOL',
    'Alpha_IX': 'HOVALFYZDKCBISGXMTRNUWQJPE',
    'Alpha_V': 'THQCNGIRAFVBLUXPYMSKOEJDZW',
    'Alpha_VI': 'BKCWIFXZMSLEAJPHRTUNQOYDGV',
    'Alpha_VII': 'WTREIPMCDONJLYZFGQXUBSAVKH',
    'Alpha_VIII': 'IPOTLGXUENWSMJYQRCFAHBVKZD',
    'Alpha_X': 'LETWCMHZOSKBDIYJVXNGAPFURQ',
    'Alpha_XI': 'FHDEPYKMVQTNBLRUXSGZJWCOAI',
    'Alpha_XII': 'YRVMOSUJIDZTBLXGNHCPWQFEKA',
    'Alpha_XIII': 'YKTEDPCGXJHAZSRWNIQOMUVBFL',
    'Alpha_XIV': 'XVZQYGOBDIUAMPJSFCNTKWHRLE',
    'Alpha_XIX': 'RQBLCXMPNKHTSFVOZEYAUDJWGI',
    'Alpha_XV': 'KHUINGLFXRZCWPJDSBYVATMQEO',
    'Alpha_XVI': 'EFNRPTSZVWMBCYKDOIQULAXGHJ',
    'Alpha_XVII': 'QCTRXZVWIYHKBUPFLJMNOSEGAD',
    'Alpha_XVIII': 'IJMBZFHPSKEVTAQDLWGCUNXORY',
    'Alpha_XX': 'OELHXRFJQSWAPGCITMNBVYZUKD'}


Do you want to save the generated alphabets to the program? (y/n) > y
2023-02-05 23:01:43,804 - __main__ - INFO - Success!
2023-02-05 23:01:43,805 - __main__ - INFO - Wrote 20 alphabets to '/home/hendrik/Documents/Github/PolyVigenere/data/alphabets.txt'.


Note:
In order to use the generated alphabets, please copy
the contents of alphabets.txt, found in '/data' to
the variable 'alphabets' in the file 'polyAlpha.py'
```


## Planned Features:<br>

    + Randomize the choice of alphabet for each character in the key.
    + Add support for enciphering/deciphering txt files.
    + 



<br>

## Notes and sources:<br>

[^src]: Source Code: [src](https://github.com/hookahtagen/PolyVigenere/blob/main/src/)
[^vigenere-cipher]: Source: [vigenere-cipher-twitch](https://steamuserimages-a.akamaihd.net/ugc/781867089027223194/99CFD48BB59612E4F6FECD0600EBE920BED846B6/?imw=512&&ima=fit&impolicy=Letterbox&imcolor=%23000000&letterbox=false)