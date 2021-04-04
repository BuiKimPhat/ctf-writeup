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

const cartesian = (...a) =>
  a.reduce((a, b) => a.flatMap((d) => b.map((e) => [d, e].flat()))); // tích đề các

function addImage(glob, result) {
  var fragment = document.createDocumentFragment();
  var img = document.createElement("img");
  img.src =
    "data:image/png;base64," +
    btoa(String.fromCharCode.apply(null, new Uint8Array(result)));
  fragment.appendChild(img);

  return glob.appendChild(fragment);
}
