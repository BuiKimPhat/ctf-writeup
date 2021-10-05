# PWNABLE

Writeup các game trong mảng pwnable mình đã từng chơi qua từ beginner

## Bắt đầu
Từ lúc mới chơi pwnable đến giờ, mình để ý các điều sau:
- File thực thi chương trình trong linux thường có dạng ELF.              
Có thể kiểm tra định dạng file và 1 số thuộc tính của file bằng lệnh:
```
file <đường dẫn file>
```
- Hệ điều hành: mình hay dùng **Ubuntu** (Linux)
- Tools:
    - **pwntools**: 1 thư viện pwn dành cho python, dùng để kết nối đến remote server, send và nhận payload, và 1 số chức năng khác phục vụ cho quá trình khai thác. Thường dùng để viết script khai thác lỗ hổng của chương trình chạy trên server sau khi đã tìm kiếm và phân tích xong lỗ hổng. [Github](https://github.com/Gallopsled/pwntools)
    - **GDB-peda**: phiên bản nâng cấp của gdb, dùng để debug code trong file thực thi + 1 số tính năng khác phục vụ cho việc khai thác lỗ hổng phần mềm. [Github](https://github.com/longld/peda)
    - **IDA Pro**: 1 công cụ Disassembler cho phép xem code assembly của file thực thi và chuyển chúng thàng mã giả C cho dễ đọc (phiên bản Pro). [Drive](https://drive.google.com/drive/folders/1-OPepikWwL2jYlkXgCq3ZmEl6mqXnvMU?usp=sharing)       
    Vì phiên bản IDA mình dùng ở link trên là cho HĐH Windows nên thường mình sẽ cài thêm **Wine** vào Ubuntu để chạy được IDA.          
    Sau khi cài IDA, sẽ có 2 phiển bản IDA trên hệ thống là IDA 32-bit và IDA 64-bit. Chú ý kiểm tra file thực thi mấy bit trước khi khởi động IDA.

## Sử dụng GDB-peda
- `pdis <tên hàm>`: hiển thị các lệnh có trong hàm đó. Lúc mới debug thì thường dùng `pdis main` để đặt breakpoints tại các hàm khác trong main cho dễ debug.
- `print <tên hàm>`: in địa chỉ gốc của hàm
- `checksec`: Xem các chế độ security của file thực thi bao gồm:
    - Canary: Lỗi tràn bộ đệm (disabled)
    - NX (Non-Executable): Không được thực thi shellcode trong chương trình (enabled)
    - RELRO (RELocation Read-Only): Đặt bảng GOT (Global Offset Table) trước vùng nhớ BSS để phòng ngừa việc ghi đè GOT bằng việc ghi tràn bộ đệm của biến toàn cục (Partial); Khiến bảng GOT chỉ có thể đọc (read-only), không thể thực hiện ghi đè lên GOT 1 hàm hay 1 ROPgadget nào cả.
    - PIE (Position Independent Executable): Vùng nhớ code luôn không đổi địa chỉ. (disabled)
    - FORTIFY
- `start`: chạy chương trình và tạm dừng trước main, sau khi setup các thanh ghi, bộ nhớ xong.
- `run` / `r`: trực tiếp chạy luôn chương trình như lúc thực thi chương trình bình thường, không tạm dừng trước main như `start`
- `continue` / `c`: tiếp tục chạy từ lúc tạm dừng đến lúc kết thúc hoặc đến lúc gặp input tiếp theo hoặc đến lúc gặp breakpoint tiếp theo
- `next` / `n`: tiếp tục chạy 1 dòng lệnh assembly tiếp theo.
- `b* <địa chỉ lệnh>`: đặt breakpoint tại địa chỉ lệnh, khi chương trình start/run thì tạm dừng ngay trước khi lệnh đó được thực hiện
- `info br`: hiển thị thông tin tất cả các breakpoints
- `del <id breakpoint>`: xóa breakpoint có id ?
- `vmmap`: xem phạm vi địa chỉ ảo của các vùng nhớ **__trong lúc chạy__** chương trình và các quyền rwx tương ứng.
- `x/<tham số> <địa chỉ>`: xem giá trị của địa chỉ cho trước. Các tham số mình thường dùng: 
    - wx (word hexa): hiển thị dưới dạng thập lục phân với độ dài 1 word (4 bytes)
    - bx (byte hexa): hiển thị dưới dạng thập lục phân với độ dài 1 byte
    - 4i (4 instructions): hiển thị 4 dòng lệnh kể từ địa chỉ đã cho
- `set $<thanh ghi>=<giá trị>`: set lại thanh ghi hiện thời trong lúc chạy chương trình thành 1 giá trị nào đó (có thể là địa chỉ nào đó). Ví dụ `set $eip=0x0804e408` thì sẽ set thanh ghi trỏ lệnh đến địa chỉ lệnh 0x0804e408, khi `next` thì chương trình sẽ nhảy đến lệnh có địa chỉ 0x0804e408 và tiếp tục thực thi từ đó.
- `stack <số ngăn xếp>`: hiển thị bộ nhớ stack với số lượng ngăn xếp cho trước
- Một số thanh ghi:
    - **RSP** (64-bit) / **ESP** (32-bit): Stack Pointer, chứa địa chỉ trên cùng stack.
    - **RIP** (64-bit) / **EIP** (32-bit): Instruction Pointer, chứa địa chỉ lệnh tiếp theo cần thực hiện.

## Sử dụng IDA PRO:
Lúc mới vào lần đầu thì sẽ có nút lựa chọn **__New__**, nhấp vào đó rồi chọn loại file là __All files__, sau đó open file thực thi mà mình cần disassemble code. OK, Ok , OK...     
Ở phần bên trái có liệt kê các hàm có trong chương trình. Double click vào hàm, sau đó tab 1-2 lần gì đó cho đến khi mình xem đã code mã giả C của hàm (Pseudo-code view).      
Trong IDA PRO, bạn có thể double-click vào 1 biến (màu xanh) để truy cập đến nguồn xuất phát sâu xa của biến đó và xem giá trị / địa chỉ của biến...

## Sử dụng pwntools:
Đầu tiên luôn phải import thư viện trước đã :v
```
from pwn import *
```
Tiếp theo, kết nối đến môi trường chạy chương trình cần khai thác:      
__Nếu chương trình chạy trên remote server__:
```
r = remote(<(string) địa chỉ của remote server>, <(int) port host chương trình trên server>)
```
__Nếu muốn chạy trực tiếp chương trình trên máy lúc khai thác__:
```
r = process(<(string) đường dẫn đến file thực thi>)
```
Thường sẽ đi chung với:
```
gdb.attach(r)
```
để debug chương trình.

- `r.recv()`: trả về 1 string, là nội dung 1 dòng chương trình in ra
- `r.recvuntil(<string>)`: trả về 1 string, là nội dung chương trình in ra cho đến khi gặp string tham số
- `r.sendline(<string>)`: gửi input đến cho chương trình nếu chương trình cần input từ bàn phím rồi nhấn enter để tiếp tục
- `r.send(<string>)`: gửi input đến cho chương trình nhưng không nhấn enter
- `r.interactive()`: tạo ra 1 shell ảo, liên tục nhận input từ client trong trường hợp chương trình liên tục yêu cầu input. Ví dụ như khi đã truy cập được shell `/bin/sh` thì có quyền liên tục nhập lệnh vào như khi tương tác với terminal, hoặc khi chương trình chạy vòng lặp vô tận mà mỗi vòng lặp có yêu cầu input...
- Hàm `p64()` / `p32()`: chuyển đổi 1 giá trị nguyên/hexa sang dạng string các kí tự ascii (cả in được lẫn không in được) (gồm 8 bytes/ 4 bytes)

## More
- Package `ascii` cho linux: Hiển thị đầy đủ bảng các kí tự ascii và mã thập phân, thập lục phân của chúng.
- Lệnh `man` trên linux: Hướng dẫn sử dụng đầy đủ của các hàm, lệnh.        
`man man` để xem danh sách các trang hướng dẫn và chi tiết.     
`man <số trang> <tên hàm/lệnh>` để xem hướng dẫn sử dụng của hàm/lệnh trong trang.

- Các shellcode `execve("/bin//sh")` trong trường hợp NX disabled:
    - 32 bit: `\x31\xC0\x50\x68\x2F\x2F\x73\x68\x68\x2F\x62\x69\x6E\x31\xDB\x31\xC9\x31\xD2\x89\xE3\x83\xC0\x0B\xCD\x80`
    - 64 bit: `\x48\x31\xFF\x57\x48\xBF\x2F\x62\x69\x6E\x2F\x2F\x73\x68\x57\x48\x31\xF6\x48\x31\xD2\x48\x89\xE7\x48\x31\xC0\x48\x83\xC0\x3B\x0F\x05`

## Các kĩ thuật khai thác / lỗ hổng bảo mật mà mình đã học được

- Pwn
    - printf format string
    - Stack overflow (Canary disabled)
    - GOT overwrite (Canary enabled)
    - ret2shellcode (NX disabled)
    - ret2libc, ROPgadget (NX enabled)

- Web
    - SQL Injection