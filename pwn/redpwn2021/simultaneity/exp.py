from pwn import *

DEBUG = True

if DEBUG:
    r = process("./simultaneity", env={"LD_PRELOAD": "./libc.so.6"})
    gdb.attach(r)
else:
    r = remote("mc.ax", 31547)

# print(r.recv())
r.interactive()