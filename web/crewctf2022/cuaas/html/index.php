<html>
	<head>
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
		<title>CuaaS</title>
		<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
		<style type="text/css">
	html, body, .container {
		height: 100%;
	}
	.container {
	    display: table;
	    vertical-align: middle;
	}
	.vertical-center-row {
	    display: table-cell;
	    vertical-align: middle;
	}
		</style>
	</head>

	<body>
		<center>
	    <div class="container">
    		<div class="vertical-center-row">
	   	 		<h1>Clean url as a Service</h1>
	     		<form method="post">
					<label class="sr-only" for="inlineFormInputGroupUsername2">Link</label>
	 				 <div class="input-group mb-2 mr-sm-2 col-sm-5">
	    				<div class="input-group-prepend">
	      					<div class="input-group-text">URL</div>
	    				</div>
	    			<input type="text" class="form-control " id="inlineFormInputGroupUsername2" name="url" placeholder="https://www.example.tld/cleanmepls?name=joe&age=13&address=very-very-very-long-string">
	  				</div>
	    			<div class="col-auto">
	      				<button type="submit" class="btn btn-primary mb-2">Clean</button>
	    			</div>
<?php
if($_SERVER['REQUEST_METHOD'] == "POST" and isset($_POST['url']))
    {
        clean_and_send($_POST['url']);
    }

	function clean_and_send($url){
			$uncleanedURL = $url; // should be not used anymore
			$values = parse_url($url);
			$host = explode('/',$values['host']);
			$query = $host[0];
			$data = array('host'=>$query);
			$cleanerurl = "http://127.0.0.1/cleaner.php";
   			$stream = file_get_contents($cleanerurl, true, stream_context_create(['http' => [
			'method' => 'POST',
			'header' => "X-Original-URL: $uncleanedURL",
			'content' => http_build_query($data)
			]
			]));
    			echo $stream;
											}


?>
	     	</form>
			</div>
	    </div>
	</center>
	</body>


</html>


