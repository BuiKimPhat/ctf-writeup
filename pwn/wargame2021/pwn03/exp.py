from pwn import *

r = remote("103.229.41.18", 5558)

payload = "AABBCCDD"
r.sendline(payload)
r.interactive()
