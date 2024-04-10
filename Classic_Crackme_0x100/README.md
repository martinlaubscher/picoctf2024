# Classic Crackme 0x100 Writeup

Points: 300<br>
Challenge Author: Nandan Desai

Description:<br>
A classic Crackme. Find the password, get the flag! Crack the Binary file locally and recover the password. Use the same password on the server to get the flag!

Hint:<br>
Let the machine figure out the symbols!

## Solution

We start by checking out the binary using the ```file``` and ```checksec``` commands (checksec is provided by pwntools). This shows us that we're dealing with a little endian 64-bit executable.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/55acccb3-f1fa-4db8-b63a-0d9e1c18d73c)

Next, we try to run the binary. It asks us for a password and then, after entering an arbitrary password, tells us that we failed (which was to be expected).<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/b55892b9-c610-4674-82c2-eba147b1a97b)

Let's have a look at the binary in Ghidra to see if we can make sense of what the program is actually doing.

I am starting at the end for this one. Looks like we are comparing the contents of two memory locations. If they are the same, we get the flag!<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/94efdfd3-08f2-472a-8f1e-7fc341c6feb4)

Now we need to take a closer look at the memory locations being compared. Looks like local_68 is a string, given in hex. So this must be the string our input is checked against. We should note two more things:<br>
1. Ghidra interprets the string as big endian, so local_68 is actually "kgxmwpbp"<br>
2. The string is not null terminated. Looking at the other, similar, variables below we notice that only uStack_39 is null terminated (we know this since the variable was declared to have 4 bytes but there are only three bytes written to it). This is important since this means that string operations will treat the whole content from local_68 to uStack_39 as one string.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/21b78d21-fdc5-4ea3-82d5-d284571a557c)

The second point mentioned above becomes relevant when we check the arguent specifying how many bytes should be compared in the memcmp function. In the decompiled code this value is stored in variable local_14. We can see that this variable contains the string length of local_68. However, as noted before, since this a string operation the function will keep counting until it reaches the null terminator, which is in uStack_39. At this point we can even calculate the length manually, and see that it is 50 (sum of the size of all the string parts, minus the null terminator).

At this point we have a pretty good idea what our input is eventually compared against, so let's have a closer look at how our input is treated. From looking at the memcmp function, we know that our input (or what it is transformed to) is eventually stored in local_a8.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/42a2c780-be8f-487f-a3d2-dccb265cce16)

In line 34, we can see that our input is stored in local_a8 when we enter it. Between lines 42 and 50 there seems to be the core of this challenge where our input is transformed in some way. Checking the two for loops (lines 42 and 43), we see that we loop over our entire input a total of three times. Inside the inner loop is where the actual transformation takes place (line 48). There is quite a lot going on, with plenty of bitwise operations as well as some standard math operations. Looking at the inner loop a bit more closely, we notice:<br>
- local_28 only depends on the index of the current character (local_10), the other values used in its calculation are hardcoded
- the same holds for local_2c (only local_28 can change, which depends on the index of the current character as shown above)
- iVar1 depends on both the index of the current character and its ASCII value. However, if we look more closely, we see that it basically just takes the ASCII value and applies an offset based on the index to it.
- the current character in local_8 is replaced by a character that is determined through applying an offset based on iVar to the character 'a' (stored in local_21). <br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/b2ea1a8f-b176-4ea4-84c2-f42244c17bbe)

From the above we can conclude that in the end there is nothing fancier happening than an offset being calculated based on the index of each character of our input, which is then applied to the 'a' character to get the transformed input. Combining all the knowledge we gained so far, we can now run the program with 50 'a' characters as the input and check the transformed input by setting a breakpoint in gdb.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/4fef86c7-a71d-4a32-8162-0130bf4afe51)

Remembering that our transformed was the first argument when calling the memcmp function, we note that our input of all 'a's has been transformed to ```addgdggjdggjgjjmdggjgjjmgjjmjmmpdggjgjjmgjjmjmmpgj```. We can further see that this is being checked against ```kgxmwpbpuqtorzapjhfmebmccvwycyvewpxiheifvnuqsrgexl``` (the second argument).
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/e8540970-358a-4018-8fb9-557596927842)

Now we have everything to crack the password, since we can simply calculate the offset between each character of the all 'a' transformed input and each corresponding character in the password check to find what we need to provide as the original input.
```
lookup = "abcdefghijklmnopqrstuvwxyz" * 2                                   #the alphabet (twice, to account for negative offsets)
password_check = "kgxmwpbpuqtorzapjhfmebmccvwycyvewpxiheifvnuqsrgexl"       #what the password is checked against
a_test = "addgdggjdggjgjjmdggjgjjmgjjmjmmpdggjgjjmgjjmjmmpgj"               #the result of what a password consisting of all a's is transformed to
offset = []
password = ""

# get the offset applied to each character
for char in a_test:
    offset.append(lookup.index(char))

#subtract the offset from the position of each character in password_check to find the character needed before the transformation
for i in range(len(password_check)):
    password += lookup[lookup.index(password_check[i])+26-offset[i]]

print(password)
```
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/f10a8cbe-c094-4b4f-9a6d-ced8596ca5ce)

Testing this, we can see that it indeed gives us the correct input:<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/b48b48a6-6733-4362-a2e8-d92f28f15358)

As a final step, all that's left to do is enter the password on the server and we can get our flag!<br>
```picoCTF{s0lv3_angry_symb0ls_45518832}```<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/40cd4dbe-5c43-41f5-adcc-81bad4bc1c61)


