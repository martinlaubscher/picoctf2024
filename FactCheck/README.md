# FactCheck Writeup

Points: 200<br>
Challenge Author: Junias Bonou

Description:<br>
This binary is putting together some important piece of information... Can you uncover that information? Examine this file. Do you understand its inner workings? 

## Solution

We start by looking at the binary given in Ghidra. Here, we can see that the program takes the start of the flag as a string and then appends various characters to it to complete the flag. <br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/fc6d474d-5bb0-4d87-a5c4-8b1c8a0f442c)
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/2d8cb543-838a-4faa-a4ca-86227c025f71)

However, the flag is not shown at the end. At this point we could reproduce the steps manually one by one, but this is cumbersome. Checking the decompiled code in Ghidra, we can see when the operations relating to the flag end (after '}' is appended to the flag string). Now, we can look up the functional offset (from main) of the operation right after the flag string has been completed:<br>
main+5d7 (in hex)<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/89847c21-b057-4714-9a2f-2c931c331ff6)

Since we now know at which point the complete flag exists in memory, we can open the binary in gdb and add a breakpoint there:<br>
b *main+0x5d7<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/92116d96-fe76-4352-b294-d32129c28624)

Finally, we run the binary in gdb (r). The complete flag is in the rax register, since it was returned by the concatenation function just executed: picoCTF{wELF_d0N3_mate_239b483f}<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/9feb1ae1-9ec3-493d-a3f5-2f0736d4e958)
