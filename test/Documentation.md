Table of Contents ( TOC )
- [Introduction](#introduction)
  - [About the author](#about-the-author)
    - [Why did I write this?](#why-did-i-write-this)
  - [What is a polyalphabetic cipher?](#what-is-a-polyalphabetic-cipher)
    - [How does it work?](#how-does-it-work)
- [Documentation](#documentation)
  - [Installation of PolyVigenere](#installation-of-polyvigenere)
    - [Requirements](#requirements)
    - [Installation](#installation)
    - [Quickstart](#quickstart)
    - [Example Vigenre2.0.py](#example-vigenre20py)
        - [Explanation: ](#explanation-)
    - [Example polyAlpha.py](#example-polyalphapy)
  

# Introduction

## About the author

What can i say about me?<br>
I'm currently 28 years old and i live in Germany. But i hate such self introductions. So i'll just leave it at that.<br>
After a long time i found my passion to code again. I dunno how but i stuck with python and i'm really enjoying it.<br>
<br>
I'm currently working on a few projects. One of them is this PolyVigenere cipher. I'm also working on a few other projects.<br>
But for now PolyVigenere is the only one i'm willing to share with the world. :D<br>
The other projects are part just for fun and some other are not ready to be shared yet.<br>
<br>
I'm also a big fan of the Linux operating system. I've been using it for a few years now and i'm really enjoying it.<br>
Windows is the best paid virus on the market. :D<br>
But hey, that's just my opinion. <br>
<br>
If you want to contact me, or if you have any questions, feel free to do so.<br>
You can talk to me on [Telegram](https://t.me/hendrik_gerhardt) or you can send me an email.<br>
If i don't answer you within a few days, please contact me again. I might have missed your message.<br>
Or i don't wanna talk to you. :D<br>
<br><br>

### Why did I write this?

That is easy to say:<br>
I wrote this program because i wanted to learn more about python and i wanted to learn more about cryptography.<br>
I also wanted to learn how to use git and github. So i thought i could combine all of this and write a program.<br>
And hey, i did. And i think it turned out pretty good.<br>
<br>
But if you think otherwise, feel free to tell me. I'm always open for criticism.<br>
And if you have any ideas for improvements, feel free to tell me. I'm always open for suggestions.<br>
<br><br>

## What is a polyalphabetic cipher?

A polyalphabetic cipher is a type of encryption technique used in cryptography that substitutes one letter of the plaintext <br> 
with multiple different ciphertext letters. Unlike monoalphabetic ciphers, which use a single fixed substitution for all letters, <br> 
a polyalphabetic cipher uses multiple substitution alphabets to encrypt the message, making it more secure and difficult to crack. <br>
<br>

### How does it work?

The functioning of a polyalphabetic cipher can be understood as follows: <br>
The plaintext message is divided into blocks and for each block, a substitution alphabet is chosen based on the position of a letter <br>
in a keyword. The letter in the plaintext is then replaced with its corresponding ciphertext letter in the substitution alphabet. This <br>
process is repeated for each letter in the plaintext, and as a result, the same letter in the plaintext will have a different ciphertext <br>
representation in different blocks. The use of multiple substitution alphabets makes it more challenging for an attacker to crack the <br>
encryption, as the mapping between the plaintext and ciphertext is not constant. This provides a higher level of security compared to <br>
monoalphabetic ciphers, where a single substitution alphabet is used for all letters. <br>
<br><br><br><br>

# Documentation

## Installation of PolyVigenere

### Requirements

PolyVigenere requires python 3.6 or higher to run. <br>
Other than that, there are no other requirements. <br>
<br>
Oh... Of course you need a keyboard and a screen to use PolyVigenere. <br>
But you have that anyway, right? How else would you read this? :D <br>
<br><br>

### Installation

For now you don't need to install PolyVigenere. You can just download the source code and run it. <br>
But i'm planning to make a pip package out of it. So you can just install it with pip. <br>
That are the plans for now. But i'm not sure if i'll do it. <br>
But who knows. Maybe i'll do it. I think it would be a good idea and it would be a good learning experience. <br>
So stay tuned. <3 <br>

### Quickstart

To use PolyVigenere, you need to download the source code. <br>
Download it to a folder of your choice. <br>
Then open a terminal and navigate to the folder where you downloaded the source code. <br>
Then run the following command: <br>
```python PolyVigenere.py``` <br>
<br>
For an example, please visit the [Example Vigenre2.0.py](#example-vigenre20py) section. <br>
or<br>
the [Example polyAlpha.py](#example-polyalphapy) section. <br>
That's it. You can now use PolyVigenere. <br>

### Example Vigenre2.0.py

```console
hendrik@example:~$ /bin/python3 /home/hendrik/Documents/Github/PolyVigenere/src/Vigenere2.0.py
Do you wanna use the default alphabet set or use a custom one? (d/c) > d
Enter 'e' for encrypt or 'd' for decrypt: e
Enter message: therussiansarecoming
Example key: 'ACBDLJ'
Enter key: ACBDLJ (<-- Is actually hidden in the terminal)
Entered message: therussiansarecoming
Encrypted message:  RVNEBEHYPMLDOYVHXYYR
hendrik@example:~$ 
```
<br>

##### Explanation: <br>
Call the program with <br><br>

```console
hendrik@example:~$ python3 Vigenere2.0.py
``` 

Then you'll be asked if you wanna use the default alphabet set or a custom one. <br>
The default alphabet set is the one that is stored in <br><br>

```console  
/src/polyAlpha.py
```

You can also use a custom alphabet set if you want to. But i don't recommend it for now, as <br>
it's not really tested yet. <br>
<br>
Then you'll be asked if you wanna encrypt or decrypt a message. <br>
Do so by entering <br><br>

```console 
e for encrypt or d for decrypt.
```

After that you'll be asked to enter a message. <br>
Enter the message you wanna encrypt or decrypt. <br>
<br>
Then you'll be asked to enter a key. <br>
Enter the key you wanna use. <br>
In this example i used the key <br><br>

```consle
ACBDLJ
```

But as i said, the key is actually hidden in the terminal and this is just for demonstration purposes. <br>

### Example polyAlpha.py

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
the variable 'alphabets' in the file 'polyAlpha.py' found in '/src'.
hendrik@example:$ 
```