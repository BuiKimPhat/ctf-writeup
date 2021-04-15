# [Silver Bullet [200 pts]](https://pwnable.tw/challenge/#6)
**__ret2libc__**

> Please kill the werewolf with silver bullet!      
> nc chall.pwnable.tw 10103     
> [silver_bullet](https://github.com/BuiKimPhat/ctf-writeup/blob/master/pwn/pwnable_tw/silverBullet_02/silver_bullet)     
> [libc.so](https://github.com/BuiKimPhat/ctf-writeup/blob/master/pwn/pwnable_tw/silverBullet_02/libc_32.so.6)        

> Viết write-up cực mất thời gian, nên bài này mình sẽ nói ngắn gọn hơn và những kiến thức đã viết ở bài trước ([Binary Gauntlet 0](https://github.com/BuiKimPhat/ctf-writeup/tree/master/pwn/picoctf/binaryGauntlet_01)) mình sẽ không lặp lại.    

## Phân tích

Sau khi chạy thử chương trình vài lần, mình có thể tóm tắt lại chức năng chương trình như sau:
1. Hiển thị menu gồm 4 lựa chọn:
    1. Create a Silver Bullet: tạo ra 1 viên đạn
    2. Power up Silver Bullet: tăng sức mạnh cho viên đạn đã tạo
    3. Beat the Werewolf: dùng viên đạn đã tạo với chỉ số sức mạnh của nó gây sát thương lên con ma sói.
    4. Return: thoát chương trình
2. Yêu cầu người dùng input 1 trong 4 lựa chọn
3. Phải tạo viên đạn ra trước để có thể bắn sói
4. Viên đạn đã tạo có thể được nâng cấp sức mạnh để gây nhiều sát thương hơn
5. Có thể bắn sói nhiều lần với chỉ số sức mạnh chỉ viên đạn đã tạo cho đến khi sói chết thì sẽ thắng.

Xem xét 1 số hàm trọng điểm của chương trình trong IDA (mình sẽ không nói kĩ về các lần in ra màn hình string cố định nếu không cần thiết):      
- main: gọi hàm menu, yêu cầu nhập input, gọi hàm tương ứng với input.        
- menu: chỉ đơn thuần in ra menu lựa chọn.
- create_bullet: Nếu chưa tạo đạn, yêu cầu nhập input max 48 kí tự và lưu vào biến `s` trên stack. Sức mạnh của viên đạn sẽ là độ dài của chuỗi `s`.
```
int __cdecl create_bullet(char *s)
{
  int result; // eax@2
  size_t v2; // ST08_4@3

  if ( *s )
  {
    result = puts("You have been created the Bullet !");
  }
  else
  {
    printf("Give me your description of bullet :");
    read_input(s, 48u);
    v2 = strlen(s);
    printf("Your power is : %u\n", v2);
    *((_DWORD *)s + 12) = v2;
    result = puts("Good luck !!");
  }
  return result;
}
```
Mình thấy dòng `*((_DWORD *)s + 12) = v2;` khá khó hiểu, nên mình sẽ thử đặt breakpoint tại dòng `printf` thứ 2 và dòng `puts` cuối cùng trong hàm `creat_bullet` rồi debug thử xem.       
```
[----------------------------------registers-----------------------------------]
EAX: 0x12
EBX: 0x0
ECX: 0x14
EDX: 0x6
ESI: 0xf7fc2000 --> 0x1d4d8c
EDI: 0x0
EBP: 0xffffce80 --> 0xffffcec8 --> 0x0
ESP: 0xffffce74 --> 0x8048c75 ("Your power is : %u\n")
EIP: 0x8048853 (<create_bullet+88>:     call   0x8048498 <printf@plt>)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x8048848 <create_bullet+77>:        mov    DWORD PTR [ebp-0x4],eax
   0x804884b <create_bullet+80>:        push   DWORD PTR [ebp-0x4]
   0x804884e <create_bullet+83>:        push   0x8048c75
=> 0x8048853 <create_bullet+88>:        call   0x8048498 <printf@plt>
   0x8048858 <create_bullet+93>:        add    esp,0x8
   0x804885b <create_bullet+96>:        mov    eax,DWORD PTR [ebp+0x8]
   0x804885e <create_bullet+99>:        mov    edx,DWORD PTR [ebp-0x4]
   0x8048861 <create_bullet+102>:       mov    DWORD PTR [eax+0x30],edx
Guessed arguments:
arg[0]: 0x8048c75 ("Your power is : %u\n")
arg[1]: 0x12
[------------------------------------stack-------------------------------------]
0000| 0xffffce74 --> 0x8048c75 ("Your power is : %u\n")
0004| 0xffffce78 --> 0x12
0008| 0xffffce7c --> 0x12
0012| 0xffffce80 --> 0xffffcec8 --> 0x0
0016| 0xffffce84 --> 0x80489b4 (<main+96>:      add    esp,0x4)
0020| 0xffffce88 --> 0xffffce94 ('a' <repeats 18 times>)
0024| 0xffffce8c --> 0x7fffffff
0028| 0xffffce90 --> 0x8048d06 --> 0x6e6947 ('Gin')
[------------------------------------------------------------------------------]
```
Có vẻ như đối với chương trình 32-bit, thứ tự nạp các tham số của hàm `printf` không phải ở trong thanh ghi nữa mà là trong stack. Mình để ý thấy tham số đầu tiên sẽ ở đỉnh stack, tham số tiếp theo ở stack tiếp theo...      
Xem tiếp breakpoint tại `puts` để hiểu hơn về dòng `*((_DWORD *)s + 12) = v2;`.     
```
[----------------------------------registers-----------------------------------]
EAX: 0xffffce94 ("aaaaaaaa")
EBX: 0x0
ECX: 0x12
EDX: 0x8
ESI: 0xf7fc2000 --> 0x1d4d8c
EDI: 0x0
EBP: 0xffffce80 --> 0xffffcec8 --> 0x0
ESP: 0xffffce78 --> 0x8048c89 ("Good luck !!")
EIP: 0x8048869 (<create_bullet+110>:    call   0x80484a8 <puts@plt>)
EFLAGS: 0x282 (carry parity adjust zero SIGN trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x804885e <create_bullet+99>:        mov    edx,DWORD PTR [ebp-0x4]
   0x8048861 <create_bullet+102>:       mov    DWORD PTR [eax+0x30],edx
   0x8048864 <create_bullet+105>:       push   0x8048c89
=> 0x8048869 <create_bullet+110>:       call   0x80484a8 <puts@plt>
   0x804886e <create_bullet+115>:       add    esp,0x4
   0x8048871 <create_bullet+118>:       nop
   0x8048872 <create_bullet+119>:       leave
   0x8048873 <create_bullet+120>:       ret
Guessed arguments:
arg[0]: 0x8048c89 ("Good luck !!")
[------------------------------------stack-------------------------------------]
0000| 0xffffce78 --> 0x8048c89 ("Good luck !!")
0004| 0xffffce7c --> 0x8
0008| 0xffffce80 --> 0xffffcec8 --> 0x0
0012| 0xffffce84 --> 0x80489b4 (<main+96>:      add    esp,0x4)
0016| 0xffffce88 --> 0xffffce94 ("aaaaaaaa")
0020| 0xffffce8c --> 0x7fffffff
0024| 0xffffce90 --> 0x8048d06 --> 0x6e6947 ('Gin')
0028| 0xffffce94 ("aaaaaaaa")
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Breakpoint 5, 0x08048869 in create_bullet ()
gdb-peda$ stack 20
0000| 0xffffce78 --> 0x8048c89 ("Good luck !!")
0004| 0xffffce7c --> 0x8
0008| 0xffffce80 --> 0xffffcec8 --> 0x0
0012| 0xffffce84 --> 0x80489b4 (<main+96>:      add    esp,0x4)
0016| 0xffffce88 --> 0xffffce94 ("aaaaaaaa")
0020| 0xffffce8c --> 0x7fffffff
0024| 0xffffce90 --> 0x8048d06 --> 0x6e6947 ('Gin')
0028| 0xffffce94 ("aaaaaaaa")
0032| 0xffffce98 ("aaaa")
0036| 0xffffce9c --> 0x0
0040| 0xffffcea0 --> 0x0
0044| 0xffffcea4 --> 0x0
0048| 0xffffcea8 --> 0x0
0052| 0xffffceac --> 0x0
0056| 0xffffceb0 --> 0x0
0060| 0xffffceb4 --> 0x0
0064| 0xffffceb8 --> 0x0
0068| 0xffffcebc --> 0x0
0072| 0xffffcec0 --> 0x0
0076| 0xffffcec4 --> 0x8
```
Qua quan sát thì sau khi dòng `*((_DWORD *)s + 12) = v2;` thực hiện, sức mạnh viên đạn đã được lưu vào địa chỉ stack thứ 12 (0xffffcec4) sau stack chứa chuỗi `s` (0xffffce94), tức là 12*4 = 48 bytes sau địa chỉ stack chứa chuỗi `s`.        
`s` được khai báo là kiểu char* nên khi ép sang địa chỉ stack (_DWORD *) và làm phép cộng 12 thì 12 cũng tự động được hiểu là số offset giữa 2 địa chỉ stack. Đối với kiến trúc 32-bit, địa chỉ 1 stack được thể hiện bằng 4 bytes = > 1 offset = 4 bytes.      

- power_up: Nếu đã tạo đạn, so sánh nếu sức mạnh > 47 thì không thể tiếp tục tăng sức mạnh, nếu sức mạnh <= 47 thì cho phép tăng sức mạnh.      
```
int __cdecl power_up(char *dest)
{
  int result; // eax@2
  char s; // [sp+0h] [bp-34h]@1
  size_t v3; // [sp+30h] [bp-4h]@1

  v3 = 0;
  memset(&s, 0, 48u);
  if ( *dest )
  {
    if ( *((_DWORD *)dest + 12) > 47u )
    {
      result = puts("You can't power up any more !");
    }
    else
    {
      printf("Give me your another description of bullet :");
      read_input(&s, 48 - *((_DWORD *)dest + 12));
      strncat(dest, &s, 48 - *((_DWORD *)dest + 12));
      v3 = strlen(&s) + *((_DWORD *)dest + 12);
      printf("Your new power is : %u\n", v3);
      *((_DWORD *)dest + 12) = v3;
      result = puts("Enjoy it !");
    }
  }
  else
  {
    result = puts("You need create the bullet first !");
  }
  return result;
}
```
Hãy tiếp tục nói rõ hơn về việc tăng sức mạnh như thế nào:      
- Ở đầu hàm, khởi tạo 1 biến char `s` cục bộ và hàm `memset` ghi đè 48 bytes đầu tiên trong bộ nhớ được biến `s` trỏ đến bằng 0x00.     
- Nhập chuỗi input rồi lưu vào `s` với max kí tự là (48 - sức mạnh).
- Dùng hàm `strncat` để ghép (48 - sức mạnh) kí tự từ chuỗi `s` cục bộ này vào chuỗi `dest` (chuỗi tạo đạn ban đầu).
- Sức mạnh mới của viên đạn = độ dài chuỗi `s` + sức mạnh cũ của viên đạn.  
- Lưu sức mạnh mới vào cùng địa chỉ bộ nhớ chứa sức mạnh cũ của viên đạn.   

- beat: Nếu đã tạo đạn, máu = máu - sức mạnh. Sau đó kiểm tra nếu máu ma sói <= 0 thì thông báo win, không thì thông báo còn sống.      

Nhìn sơ qua main và các hàm trong đó, ta có thể thấy chương trình chẳng đọc file flag hay gì cả. Dù có bắn chết sói và chiến thắng thì cùng lắm cũng chỉ hiện dòng chữ "Oh ! You win !!". Thứ mình cần là flag, không phải sự an ủi vô dụng này :)      
Nếu như thế thì mình chỉ còn cách lấy shell trên remote thôi.       
Đầu tiên thì mình nghĩ đến ret2shellcode, nhưng sau khi `checksec` thì có vẻ như ta phải đi hướng khác rồi.      
```
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : disabled
RELRO     : FULL
```
Chế độ bảo vệ NX đã được bật, nên mình không thể thực thi được shellcode trong chương trình rồi hic :TT Phải tìm cách bypass NX thôi            
Tuy nhiên, nếu `pdis main` ta có thể thấy chương trình vẫn có lệnh `ret` ở cuối cùng. Hmm... vậy có 1 cách nào đó chạy được các lệnh cần để thực hiện lấy shell nhưng không cần phải tự viết shellcode và đưa vào input không nhỉ?      
Sau khi tìm hiểu, mình đã tìm thấy kĩ thuật __ret2libc__.  

Kĩ thuật __ret2libc__: dùng chính những lệnh trong file libc mà chương trình load để ghi đè vào return address nhằm khai thác chương trình.       




