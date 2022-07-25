<?php

if ($_SERVER["REMOTE_ADDR"] != "127.0.0.1"){

die("<img src='https://imgur.com/x7BCUsr.png'>");

}

echo "<br>There your cleaned url: ".$_POST['host'];
echo "<br>Thank you For Using our Service!";

function tryandeval($value){
                echo "<br>How many you visited us ";
                eval($value);
        }


foreach (getallheaders() as $name => $value) {
	if ($name == "X-Visited-Before"){
		tryandeval($value);
	}}
?>
