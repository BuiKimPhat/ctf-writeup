# JS Kiddie (400 points)
*Newbie*

### Đề
The image link appears broken... https://jupiter.challenges.picoctf.org/problem/17205 or http://jupiter.challenges.picoctf.org:17205

### Hint
- This is only a JavaScript problem. (hint có ích vl XD)

## Giải 
Trang chủ của web chỉ có 1 ô input và submit.      
Nhập lung tung vào cái ô input thì nó hiện ra icon ảnh vỡ (chắc là link ảnh bị lỗi...)      
F12 Inspect cái ảnh để xem link nó trỏ tới đâu thì thấy 1 chuỗi dài loằng ngoằng không giống với link https thông thường lắm. Chuỗi bắt đầu với `data:image/png;base64` nên mình nghĩ đây là dạng ảnh png với nội dung là cái dãy kí tự dài loằng ngoằng được mã hóa base64 ở phía sau.     
Tiếp tục inspect phần script trong html thì thấy họ có cho sẵn 1 biến bytes (global scope nên có thể được sử dụng trong console) và 1 hàm assemble_png 1 tham số.       
Để ý trong script có phần họ dùng jQuery `$.get("bytes", function...` . Theo mình nhớ thì lệnh get là dùng để gọi 1 HTTP Request với phương thức GET, nên mình thử truy cập vào link https://jupiter.challenges.picoctf.org/problem/17205/bytes thì địa chỉ này có tồn tại thật, trong đó có 1 chuỗi các số kì lạ gì đó cách nhau bằng dấu cách ?       
> 87 130 78 188 0 84 26 157 143 239 249 82 248 212 239 82 195 80 1 207 13 6 1 0 119 243 73 193 78 36 133 108 85 0 0 14 0 186 68 0 0 222 0 243 0 24 174 163 126 0 133 252 137 177 121 10 0 0 0 237 73 63 0 100 96 20 3 224 59 171 16 114 0 0 0 69 0 68 68 147 137 179 110 112 74 121 238 65 1 0 156 0 155 0 95 120 0 233 226 40 78 194 248 44 84 0 208 13 41 72 138 59 164 98 71 0 209 0 99 176 97 120 202 0 135 192 54 101 64 252 81 71 205 10 243 133 30 22 125 237 3 93 90 42 73 221 25 114 243 0 116 22 4 3 59 75 188 119 169 221 161 184 178 2 73 73 231 45 14 99 102 153 166 178 206 54 127 84 240 191 220 10 163 81 64 206 128 132 102 197 72 127 239 253 78 93 8 22 239 207 146 111 143 239 27 243 28 0 173 159 196 48 247 28 84 98 63 52 171 214 214 26 233 254 65 106 111 59 73 255 148 111 103 91 20 206 222 70 252 199 161 124 245 188 102 81 159 119 174 51 190 243 55 243 156 249 124 125 2 143 191 27 119 139 126 88 18 247 171 227 72 66 54 251 0 80 171 146 113 173 4 79 211 216 214 122 119 115 225 45 24 54 44 76 43 253 5 235 104 248 96 8 229 200 75 64 233 217 23 87 40 254 187 107 181 200 181 233 181 81 231 171 165 82 254 196 239 51 43 114 170 73 249 50 114 201 138 64 11 203 155 192 249 226 35 188 156 223 40 217 67 75 100 45 93 102 169 13 34 197 80 175 210 128 137 201 167 45 140 82 171 56 212 17 126 113 139 229 127 223 181 15 0 116 221 186 219 230 56 233 31 15 249 74 119 152 44 41 226 60 35 253 172 97 32 137 233 165 35 181 104 80 217 56 186 205 212 15 64 81 230 230 153 62 251 251 47 151 141 108 32 25 65 11 253 119 201 147 243 11 31 247 233 54 126 217 136 141 191 226 137 213 131 239 100 145 151 150 119 124 159 203 190 63 18 170 210 175 122 223 223 114 124 59 93 245 177 100 15 57 63 239 165 144 13 149 32 198 39 52 53 113 97 91 186 76 91 74 207 133 208 0 245 241 245 73 122 193 223 159 82 175 241 159 231 205 24 92 75 11 247 77 55 170 7 95 127 143 96 207 242 142 153 226 242 93 163 110 185 26 188 4 178 102 159 97 53 58 186 172 239 6 78 215 65 156 90 150 112 205 73 76 149 163 159 242 45 147 16 210 49 254 82 126 200 30 62 190 230 2 86 171 181 197 185 132 170 153 82 191 154 235 147 55 57 92 252 48 207 118 191 170 253 53 127 94 143 122 230 254 154 151 186 55 160 132 126 57 183 217 129 181 95 255 35 223 50 70 77 107 100 203 17 61 163 17 227 147 182 184 79 126 239 28 115 159 254 111 90 250 14 206 185 137 187 141 231 211 241 249 39 99 131 95 210 50 147 241 95 127 103 239 113 165 223 164 245 35 231 132 166 220 241 207 67 178 148 29 156 94 194 74 222 110 0 243 107 158 173 214 210 249 84 66 107 40 0 203 138 164 0 241 9 109 147 207 85 29 204 0         
     
Quay lại trang chủ, vô console gõ thử biến **bytes** chứa gì, hóa ra nó là mảng chứa mỗi con số trong cái dãy số kia thôi. Họ tách từng số ra bởi dấu cách rồi nhét vô mảng :v Tổng cộng 720 số.        
Giờ đến phầm mệt mỏi nhất, đọc hiểu cái hàm assemble kia... 
```
var LEN = 16;
var key = "0000000000000000";
var shifter;
if(u_in.length == LEN){
    key = u_in;
}
```
`LEN` là độ dài của `key`, `key` mặc định là 16 số 0. Nếu tham số của hàm có độ dài là 16 thì hàm mới lấy tham số làm `key`. Mình đoán là mình phải tìm cái chuỗi nào đó có 16 kí tự để thay đổi `key`, chứ nhập bậy bạ vào thì cũng không cho kết quả đúng.      
Cuối hàm có 1 đoạn:
```
document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
```
`String.fromCharCode` là hàm dùng để chuyển từ hệ thập phân (bytes) sang UTF-16. `btoa()` dùng để mã hóa base64 cho chuỗi. Dòng này có vẻ như dùng để chuyển từng phần tử trong mảng sang UTF-16, ghép mảng `result` lại thành chuỗi rồi mã hóa sang base64.

Phần code còn lại mình lười đọc quá nên đọc sơ sơ, cứ thử số rồi đoán hàm nó làm gì :)))       

Có 2 dòng code mình để ý:
```
shifter = key.charCodeAt(i) - 48;
```
*Biến `shifter` chứa mã bytes của phần tử thứ i trong chuỗi `key` - 48.* Ví dụ như chuỗi `key` ban đầu có phần tử thứ i là "0" (có bytes là 48), trừ đi 48 nữa là bằng 0. 
```
result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i]
```
*1 phần tử nào đó trong mảng `result` được gán bởi 1 phần tử nào đó trong mảng byte @@*

OK, mình sẽ thử định nghĩa lại cái hàm này để nó trả về cái `result` sau khi chạy thử nó ra cái gì. 
```
function assemble_png(u_in){
    var LEN = 16;
    var key = "0000000000000000";
    var shifter;
    if(u_in.length == LEN){
        key = u_in;
    }
    var result = [];
    for(var i = 0; i < LEN; i++){
        shifter = key.charCodeAt(i) - 48;
        for(var j = 0; j < (bytes.length / LEN); j ++){
            result[(j * LEN) + i] = bytes[(((j + shifter) * LEN) % bytes.length) + i]
        }
    }
    while(result[result.length-1] == 0){
        result = result.slice(0,result.length-1);
    }
    document.getElementById("Area").src = "data:image/png;base64," + btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
    return result;
}
```

Chạy thử với tham số chuỗi 16 số 0, kết quả là y hệt cái mảng bytes ban đầu, chỉ khác là phần tử cuối cùng không có số 0 nên chỉ có 719 phần tử @@       
Chạy thử với tham số "1000000000000000", phần tử đầu tiên thay đổi thành 195, phần tử tiếp theo thay đổi là phần tử thứ `16` đổi thành 85. Sau khi chạy thử với các chuỗi số khác nhau, mình nhận ra là có thể nó chia cái mảng `bytes` 720 phần tử đó ra làm nhiều tập con, mỗi tập 16 phần tử, tổng cộng 45 tập con,  thay đổi phần tử ở vị trí nào trong `key` thì phần tử ở vị trí tương ứng trong `result` cũng thay đổi theo. Nhưng thay đổi thế nào?       
Tiếp tục chạy thử với tham số "2000000000000000", phần tử đầu tiên thay đổi thành 85... Khoan đã, số 85 có vẻ quen, nó là phần tử thứ `16` trong lần chạy trước và là phần tử thứ `32` trong bytes. Vậy phần tử đầu tiên trong tập con đầu tiên của `result` sẽ bằng phần tử đầu tiên trong tập con thứ 2 (=`shifter`) của `bytes`. Và mình đoán là những vị trí khác trong những tập con cũng tương tự như vậy...      
Vậy là mình đã biết được quy luật của hàm assemble, thế giờ làm sao để tìm cái mảng bytes tạo ra cái hình :v ??

Theo mình tìm hiểu, thì mọi bức ảnh đều có 1 cái header dùng để nhận biết cái file này là file ảnh, và cái header đó có dạng hex (thập lục) chứa trong phần đầu của file ảnh. Bức ảnh mình cần tìm có dạng png nên mình nghĩ header của nó cũng giống với header của các file ảnh png khác. Tức là nếu bằng cách nào đó mình tìm ra số lần dịch chuyển các bytes đầu tiên của mảng `bytes` sao cho giống với các bytes đầu tiên của file ảnh png thì hy vọng các bytes còn lại trong mảng sẽ đúng và tạo ra được bức ảnh :v     
Mình sẽ lấy 1 cái ảnh mẫu có định dạng png rồi xem mã hex của nó như thế nào. Đa số các file ảnh png đều có phần hex đầu (header) giống nhau nên mình chỉ cần xem vài dòng đầu.     
```
hexdump Leo.png -C | head -n 2
```
Kết quả:
```
00000000  89 50 4e 47 0d 0a 1a 0a  00 00 00 0d 49 48 44 52  |.PNG........IHDR|
00000010  00 00 00 8b 00 00 00 8c  08 02 00 00 00 c3 7e cd  |..............~.|
```
*Mình để ý các file png chỉ có dòng đầu là giống nên mình chỉ xét dòng đầu (16 ký tự mã hex, vừa đủ 16 kí tự trong `key` :))))*

Chuyển hex về bytes (decimal), ta được mảng bytes header png:
```
[137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82]
```
Rồi bây giờ vấn đề là làm sao để biết được `shifter` là mấy để tập con đầu tiên của mảng `result` giống với mảng header??? **Bruteforce** thôi (vì chỉ có 45 tập con chứ mấy) :v       
Mình có viết 1 hàm để tiện cho việc bruteforce:
```
function dissemble_png() {
  var LEN = 16;
  var png = [137, 80, 78, 71, 13, 10, 26, 10, 0, 0, 0, 13, 73, 72, 68, 82]; // png files' header
  var code = [];
  for (var i = 0; i < LEN; i++) {
    console.log("Fit " + i);
    code.push([]);
    for (var j = 0; j < 45; j++) {
      if (png[i] == bytes[j * LEN + i]) {
        console.log(String.fromCharCode(j + 48));
        code[i].push(String.fromCharCode(j + 48));
      }
    }
  }
  return code;
}
```
*Hàm trả về 1 mảng gồm các mảng con, mảng con thứ i chứa các kí tự khả thi ở vị trí thứ i trong `key`*
Tạo ra các `key` bằng cách nhân tích đề các của các mảng con với nhau, tạo ra nhiều chuỗi khả thi (các chuỗi có header giống png, còn nội dung thì không biết có ra được ảnh không, phải bruteforce thử từng chuỗi mới biết được).      
Sau khi dạo quanh trên mạng tìm code tính tích đề các cho nhanh thì được em này gọn gàng phết
```
const cartesian = (...a) =>
  a.reduce((a, b) => a.flatMap((d) => b.map((e) => [d, e].flat()))); // tích đề các
```
*Code dùng các syntax của ES6 nhé...*
Gọi hàm để trả về các chuỗi khả năng `key`, lưu vào mảng `output`:
```
let output = cartesian(...dissemble_png()).map(e => e.join(""));
```
*Ra được mảng gần 300 chuỗi khả năng :v*        

Giờ thì lặp qua từng phần tử rồi submit vào, mỗi lần submit thì add cái ảnh png tương ứng vào (để khi submit đúng thì vẫn nhìn thấy chứ không bị ghi đè)        
Hàm đơn giản để thêm ảnh vào element `glob`, với mảng `result` tương ứng (trả về từ hàm assemble sau khi định nghĩa lại):
```
function addImage(glob, result) {
  var fragment = document.createDocumentFragment();
  var img = document.createElement("img");
  img.src =
    "data:image/png;base64," +
    btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
  fragment.appendChild(img);

  return glob.appendChild(fragment);
}
```

Bước cuối cùng, lặp qua tất cả các chuỗi khả năng, gọi hàm assemble để lấy `result` sau đó thế vào hàm addImage để thêm ảnh vào html thôi ~~        
*Thêm id="main" vào `<body>` để tiện cho việc thêm ảnh trước*
```
for (var i=0;i < output.length;i++) addImage(document.getElementById("main"), assemble_png(output[i]));
```

Kết quả cho 1 ảnh nhìn thấy được (QR code) có src:
> data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAXIAAAFyAQAAAADAX2ykAAACiUlEQVR4nO2bXYqjQBSFvzsKeSxhFtBLKXc2ZEmzA11KFhCwHgPKmYeyWpOh6W4wThzuhQRjfYQDxal4f2LiO9H/+BYOzjvvvPPOO+/8R7zNUWMtQG9m1qYaSGWt3VGP8xvzUZI0gM5mRhwqQbgZUEmSdM8/W4/zG/Pp3aFUsjbcTOdiZzOr99bj/DZ8/fDZCFejb65YFNjeepx/Np9OUvfE73d+T774NwhIAOFqxMtJwFSLBOsSyKvpd/5LfG9mZg2UrQVr00nWMuXH5331OL8Rn/27cmjfYNm1+Yr7Auar6Xf+K7y1gLXJckJkLQBhLIlxMyOvqt/5D0NzjEAYURfmK+JQ5ZyYKCmnyN2r6Xf+kyjFi0rSUIk4AFEjQKXVm+/vcfm1f5e1bOLJ1C0Lr6nf+Q8j+3c2LNm6S0FSXZDUlSKl+/dofNnLIC2/uquFOAB+Ph+WL/WNZIh0Ev3bzSBcHwuXO+lxflu+PD8PrI7m4umRfDR3wZ+fD81bC0A6yayZcidJXaqxX7oZ8eL9o4Py88b1TTUaYQRSjWCqiQJ6q2Tx9256nN+Wfz+f79JcDTDfC6PXN/4HfrI5SUqll9A3IF1O0rmZvL9wTD6fz0YYa/UGEIRBNVpeyK+Tz+ccmZ9Lk7mqMdlStZqP5mHy+bpj8sW/OaoRUpOPZiNMNaSfI+92fj39zn+JX81PvpVKVm4thBH6t/GBf7Ye5zfmy/yktctaMqPP47K763H+Oby6VM9v0twO1rn5Z3qc35rPTQagX6aek89fHZT/a34yDnO6ZIRrbfFSQ9RUuFfT7/wnsf7zCe+twdIkzI3DpfHg9auD8Y/zk/NVGO/vVV7fcN5555133vnt+D+FHX4owiiKwgAAAABJRU5ErkJggg==

Lên google search công cụ decode QR online (https://zxing.org/w/decode.jspx) rồi paste src vào, thế là ra flag :')
> picoCTF{066cad9e69c5c7e5d2784185c0feb30b}







