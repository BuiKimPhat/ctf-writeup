# JaWT Scratchpad (400 points)
*Newbie*

### Đề 
> Check the admin scratchpad! https://jupiter.challenges.picoctf.org/problem/61864/ or http://jupiter.challenges.picoctf.org:61864
### Hint
- What is that cookie?
- Have you heard of JWT?

## Giải
Sau khi truy cập đường link, ta sẽ đến 1 trang web có 1 ô input và 1 vài thông tin, link gì đó...
Nhập thử admin vào rồi enter, nó báo lỗi không phải admin và không cho. Nhập chuỗi khác mới được, nó sẽ chuyển sang phần textarea chả biết để làm gì (chắc ghi chú).   
Hint có liên quan gì đó đến cookie, nên ta sẽ thử kiểm tra trong cookie có gì hot.      
Sau khi submit cái ô đăng nhập đó, thì trong cookie xuất hiện thêm 1 trường gọi là jwt (có trong hint).     
Sau khi tìm hiểu thì mình biết JWT là 1 token gồm 3 phần header, payload và signature. Header và payload được mã hóa bằng base64URL, còn signature là sự kết hợp giữa header, payload và secret nào đó, sau đó được thường được encode bằng HS256?...     
Trong lúc tìm hiểu thì mình tìm thêm được các trang hữu ích như https://jwt.io/ , https://gchq.github.io/CyberChef/ ... dùng để encode, decode các thứ...   
Mình copy thử cái jwt trong cookie rồi quăng vào https://jwt.io/ thì thấy nó decode ra được header: thuật toán encode là HS256, payload: trường user có giá trị là thứ mình nhập trong ô đăng nhập. Vậy ra trang web nhận biết được admin hay không là qua cái payload này.

Lúc này mình nhận ra vấn đề là: cần tìm secret để tạo 1 jwt khác có user là admin.

Tìm kiếm loanh quanh trên Google cái bypass jwt thì thấy 1 bài viết khá hữu ích. https://www.sjoerdlangkemper.nl/2016/09/28/attacking-jwt-authentication/       
Cụ thể là mình có thể bruteforce ra cái secret của jwt dùng **JohnTheRipper** (Lúc này mới nhận ra là ở trang chủ của cái JaWT Scratchpad nó có để 1 đường dẫn phía dưới ở chữ *John* liên kết đến github của JohnTheRipper).

Cài đặt JohnTheRipper (Hướng dẫn trong bài viết mình đã đề cập ở trên, cài bản github sẽ ổn định hơn, nếu cài bản khác lúc chạy dễ lỗi):
```
git clone https://github.com/magnumripper/JohnTheRipper
cd JohnTheRipper/src
./configure
make -s clean && make -sj4
cd ../run
./john jwt.txt
```

Lần đầu sử dụng John, thử quăng cả đoạn jwt vào rồi cho chạy john với file text chứa jwt:  
`./john jwt.john`     
Kết quả là chờ 10p vẫn chưa ra được cái secret nào nếu dùng setting wordlist mặc định của JohnTheRipper (toàn mấy chữ tào lao ko có nghĩa)....      
Sau khi tìm hiểu thì mình tìm ra được 1 wordlist khác có tên là rockyou.txt, lên google search rồi tải về rồi chạy thử với `--wordlist="rockyou.txt"`       
`./john jwt.john --wordlist="rockyou.txt"`      
Và nó lại nhanh vcl... vừa chạy là ra kết quả *ilovepico*   
Sau đó mình quay lại trang https://jwt.io/ rồi tạo 1 jwt mới với secret này và payload là user: admin
Thay jwt này vào cookie, refresh lại trang, thế là ra flag UWU
> picoCTF{jawt_was_just_what_you_thought_1ca14548}
