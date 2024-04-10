

We start by checking out the binary using the ```file``` and ```checksec``` commands (checksec is provided by pwntools). Thisshow us that we're dealing with a little endian 64-bit executable.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/55acccb3-f1fa-4db8-b63a-0d9e1c18d73c)

Next, we try to run the binary. It asks us for a password and then, after entering an arbitrary password, tells us that we failed (which was to be expected).<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/b55892b9-c610-4674-82c2-eba147b1a97b)

Let's have a look at the binary in Ghidra to see if we can make sense of what the program is actually doing.

I am starting at the end for this one. Looks like we are comparing the contents of two memory locations. If they are the same, we get the flag!<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/94efdfd3-08f2-472a-8f1e-7fc341c6feb4)

Now we need to have a closer look at the memory locations being compared. Looks like local_68 is a string, given in hex. So this must be the string our input is checked against. We should note two more things:<br>
1. Ghidra interprets the string as big endian, so local_68 is actually "kgxmwpbp"<br>
2. The string is not null terminated. Looking at the other, similar, variables below we notice that only uStack_39 is null terminated (we know this since the variable was declared to have 4 bytes but there are only three bytes written to it). This is important since this means that string operations will treat the whole content from local_68 to uStack_39 as one string.<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/21b78d21-fdc5-4ea3-82d5-d284571a557c)

The second point mentioned above becomes relevant when we check the arguent specifying how many bytes should be compared in the memcmp function. In the decompiled code this value is stored in variable local_14. We can see that this variable contains the string length of local_68. However, as noted before, since this a string operation the function will keep counting until it reaches the null terminator, which is in uStack_39. At this point we can even calculate the length manually, and see that it is 50 (sum of the size of all the string parts, minus the null terminator).<br>

At this point we have a pretty good idea what our input is eventually compared against, so let's have a closer look at how our input is treated. From looking at the memcmp function, we know that our input (or what it is transformed to) is eventually stored in local_a8.<br>

![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/42a2c780-be8f-487f-a3d2-dccb265cce16)

