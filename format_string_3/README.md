# format string 3 Writeup

Points: 300<br>
Challenge Author: SkrubLawd

Description:<br>
This program doesn't contain a win function. How can you win?

Hint:<br>
Is there any way to change what a function points to?

## Solution

Looking at the provided source code, we can see a suspicious variable normal_string, which is "/bin/sh". This suggests that we're meant to pop a shell. We can also see that this string is passed as an arguments for the final puts call. Knowing this (and with the hint to have a function point somwhere else), we can deduct that we need to change what the final puts call points to from puts(normal_string) to system(normal_string).<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/6b488607-2679-440f-b86e-002164e20b58)

Since puts is a libc function, it gets called via its got (global offset table) entry. if we can change this entry to point to system instead, we can pop a shell!

So, we check the got entry for puts in radare2 and see that its stored at 0x404018

Next, we need to find a way to write to this address. The printf call in main looks like a good target since it's missing a format specifier.

By fuzzing the input with something like:<br>
python3 -c 'print("A"*8 + ".%p"*50)' | ./format-string-3<br>
we can find that we control the offset at 38

Next, we need to determine the address of the system call at runtime. Luckily, the program "leaks" the address of setvbuf after it has been loaded. Now we can check the static offset from the libc start address and can determine the start address of libc at runtime as below:
subtract static libc setvbuf offset from leaked libc setvbuf address to find libc start address at runtime <br>
-> readelf -s libc.so.6 | grep setvbuf<br>
-> 1300: 000000000007a3f0   608 FUNC    WEAK   DEFAULT   16 setvbuf@@GLIBC_2.2.5<br>
-> leaked_address - 0x7a3f0 = loaded_libc_start

In a similar fashion, we can now calculate the address of the system call at runtime:<br>
add static libc system() offset to libc_start to find actual address of system call<br>
-> readelf -s libc.so.6 | grep system<br>
-> 1511: 000000000004f760    45 FUNC    WEAK   DEFAULT   16 system@@GLIBC_2.2.5<br>
-> libc_start + 0x4f760 = system_call<br>

Finally, we have everything together to write our exploit in python using pwntools!
