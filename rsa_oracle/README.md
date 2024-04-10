# rsa_oracle Writeup

Points: 300<br>
Challenge Author: Geoffrey Njogu

Description:<br>
Can you abuse the oracle? An attacker was able to intercept communications between a bank and a fintech company. They managed to get the message (ciphertext) and the password that was used to encrypt the message.<br>
After some intensive reconassainance they found out that the bank has an oracle that was used to encrypt the password and can be found here nc titan.picoctf.net 62628. Decrypt the password and use it to decrypt the message. The oracle can decrypt anything except the password.

Hints:
1. Crytography Threat models: chosen plaintext attack.
2. OpenSSL can be used to decrypt the message. e.g openssl enc -aes-256-cbc -d
3. The key to getting the flag is by sending a custom message to the server by taking advantage of the RSA encryption algorithm.
4. Minimum requirements for a useful cryptosystem is CPA security.

## Solution

From the challenge description and hints, we know that this task somehow revolves around conducting a chosen plaintext attack against RSA encryption. Since we can have any plaintext message encrypted by the oracle, we can craft specific plaintext messages, encrypt them using the public key, and analyze the encrypted outputs to deduce information that is useful for us. Another key here is RSA's multiplicative property. Assuming we have two numbers, a and b, this essentially means that ```encrypted(a) * encrypted(b) = encrypted(a * b)```.<br>
In our case, for example: ```encrypted(password) * encrypted(2) = encrypted(password * 2)```<br>

Now, the oracle can also decrypt any message - except the password, but the password multiplied by 2 should be no issue, right? Correct! This means by calculating the result of ```encrypted(password) * encrypted(2) = encrypted(password * 2)``` and submitting this for decryption, we get the decrypted password multiplied by two. Then, we can simply divide this by two and convert the result to utf-8 and we have the password: ```da099```<br>
Below a script that does all of these steps. <br>
```
from pwn import *

def encrypt(p, value):
    p.sendline('E')
    p.sendline(value)
    p.recvuntil(') ')
    received = int(p.recvline().strip())
    return received

p = remote('titan.picoctf.net', 62628)

password = 4228273471152570993857755209040611143227336245190875847649142807501848960847851973658239485570030833999780269457000091948785164374915942471027917017922546
two = encrypt(p,b"\x02")

password_mult = password * two

p.sendline('D')
p.sendline(str(password_mult))

p.recvuntil('(c ^ d mod n): ')
password_mult_decrypted = int(p.recvline().strip(),16)
p.close()
password_plain_int = password_mult_decrypted // 2

word_size = (len(hex(password_plain_int))-2)*4

password_plain = pack(password_plain_int, word_size, 'big').decode("utf-8")

print(f"\nplaintext password: {password_plain}")
```
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/0f59d8be-08ba-4474-80de-9c87f423d421)

As a final step, all that's left to do is decrypt the secret to get our flag:
```picoCTF{su((3ss_(r@ck1ng_r3@_da099d93}```
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/d93dc4ca-29cd-4380-981d-86c2a3ab1876)
