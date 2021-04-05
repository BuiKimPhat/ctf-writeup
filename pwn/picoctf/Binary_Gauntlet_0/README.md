# Binary Gauntlet
Hiện tại thì server của pico đã xóa bài này và update thành các bài khác nên mình không thể tìm lại link đề bài và submit được nữa. Mình nhớ đại khái là server chạy file chương trình gauntlet. Nhiệm vụ của chúng ta là tìm được flag được lưu trên server. [gauntlet](https://github.com/BuiKimPhat/ctf-writeup/blob/master/pwn/picoctf/Binary_Gauntlet_0/gauntlet)

## Việc đầu tiên cần làm là phân tích file thực thi:      
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
Dòng này có ý nghĩa: File gauntlet là file có định dạng ELF (file thực thi trên linux), 64 bits, có thể chạy trên kiến trúc x86-64, bộ nhớ được liên kết động...


- Vì file là 64 bits, ta dùng IDA Pro 64 bits để disassemble file và xem code C mã giả để dễ tìm kiếm và phân tích lỗi      
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
## Bắt đầu phân tích chương trình và tìm lỗ hổng:
Những thứ sau đây đều là ý kiến của riêng mình và chưa chắc sẽ đúng, có những thứ mình không biết hoặc không ảnh hưởng nhiều thì mình sẽ bỏ qua.        
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

### Phân tích luồng thực thi assembly bằng GDB-peda:
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
Well, hầu hết tất cả mọi chế độ bảo vệ đều đã bị tắt => file có khá nhiều hướng để khai thác. Ở đây, mình sẽ nhắm vào khai thác NX. Nếu NX đã tắt, mình có thể thực thi chính shellcode của mình trong chương trình. Còn về shellcode là gì, thì mình sẽ nói sau trong phần [viết shellcode](#shell-code).

### [Viết shellcode để khai thác lỗ hổng](#shell-code):








