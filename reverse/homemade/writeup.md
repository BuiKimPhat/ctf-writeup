Disassemble file thực thi và xem 1 lượt code, ta dễ dàng thấy được để đáp ứng được điều kiện đến dòng "Congrats" (Chúc mừng) thì đầu tiên cần phải nhập username là "pu55yS14yer69"

Cái tiếp theo cần nhập là password. Sau khi nhập đúng username thì đã vượt qua điều kiện if đầu tiên. Trong đó, có 1 vòng lặp 52 lần để xử lí từng kí tự của password và chuyển giá trị password thành 1 giá trị số nguyên khác và lưu vào như 1 phần tử trong mảng. => có thể password sẽ có 52 kí tự

Tiếp theo, có 1 vòng lặp cũng 52 lần và check từng phần tử trong mảng vừa lưu với 1 giá trị nào đó bắt đầu từ biến v9 (biến có giá trị -700416). Ta để ý thấy các biến sau cũng có giá trị nguyên tương tự, từ v9 -> v60 (52 biến) => các phần tử đó sẽ so sánh với các biến này (xem như là 1 mảng gồm 52 phần tử).
Nếu cả 52 cặp kí tự đều bằng nhau thì ta sẽ in được dòng "Congrats!". Ngược lại thì "Never give up".

```
  v9 = -700416;
  v10 = -724992;
  v11 = -679936;
  v12 = -704512;
  v13 = -786432;
  v14 = -770048;
  v15 = -491520;
  v16 = -483328;
  v17 = -483328;
  v18 = -671744;
  v19 = -761856;
  v20 = -671744;
  v21 = -692224;
  v22 = -483328;
  v23 = -692224;
  v24 = -671744;
  v25 = -483328;
  v26 = -757760;
  v27 = -671744;
  v28 = -757760;
  v29 = -708608;
  v30 = -483328;
  v31 = -499712;
  v32 = -671744;
  v33 = -757760;
  v34 = -483328;
  v35 = -729088;
  v36 = -696320;
  v37 = -671744;
  v38 = -741376;
  v39 = -761856;
  v40 = -499712;
  v41 = -499712;
  v42 = -778240;
  v43 = -622592;
  v44 = -483328;
  v45 = -495616;
  v46 = -778240;
  v47 = -696320;
  v48 = -749568;
  v49 = -503808;
  v50 = -516096;
  v51 = -671744;
  v52 = -495616;
  v53 = -692224;
  v54 = -479232;
  v55 = -503808;
  v56 = -495616;
  v57 = -483328;
  v58 = -495616;
  v59 = -679936;
  v60 = -794624;
```

Thế mục đích của bài là cần nhập password sao cho giá trị sau khi biến đổi lần lượt bằng các giá trị v9 đến v60. Ta có thể thử đảo ngược các phép tính lại để tìm ra được kí tự ban đầu trước khi biến đổi.
Thử với kí tự đầu:
-700416 >> 9 = -1368
-1368 / -8 = 171
171 - 69 = 102 (DEC của kí tự "f")
=> có thể là kí tự "f" trong "flag{"

Làm tương tự với các giá trị còn lại (có thể viết chương trình), ta được password là:   
`flag{w311_u_d1d_1t_th15_t1me_pu55yS14yer69_4d06414a}`