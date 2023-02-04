## Polyalphabetic Cipher Encrypter/Decrypter

### Description:<br>
<sup>This program allows for encryption and decryption of plaintext messages <br>
using a polyalphabetic cipher. The program uses an alphabet dictionary <br>
to define the different alphabets for each character in the key. The <br>
key is then used to shift the corresponding character in the plaintext <br>
by one place for encryption, or by one place in reverse for decryption. <br>
</sup>
### Usage:<br>
<sup>
    + Define the alphabets dictionary with the desired mapping of key characters <br>
    to their corresponding alphabets.<br>
</sup>
<br>
<sup>
    + Specify the key to be used for encryption/decryption.<br>
</sup>

<sup>
    + Call the poly_vigenere_encrypt function with the plaintext message to be <br>
    encrypted and the key, along with the alphabets dictionary. The encrypted <br>
    message will be returned.
</sup>
<br>
<sup>
    + Call the poly_vigenere_decrypt function with the encrypted message and the <br>
    key, along with the alphabets dictionary. The decrypted message will be returned. <br>
</sup>

<sup><br>
    + Note: This program only works with single-character mappings of key characters to <br>
    alphabets, and does not support multiple characters per alphabet.
</sup>
