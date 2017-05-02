<?php
/*
Convert LVTagger NER output format sentences:
	jauni	null	O
	jautājumi	null	O
	par	null	O
	Kalifornijas	null	location
	ūdensapgādes	null	O
	projektu	null	O
to:
	jauni jautājumi par Kalifornijas|LOC ūdensapgādes projektu 

*/

$inputFile 	= $argv[1];

$in  = fopen($inputFile, "r") or die("Can't open input file!");
$out = fopen($inputFile.".pipe", "a") or die("Can't create output file!");

while (($token = fgets($in)) !== false) {
	
	if($token == "\n"){
		
		fwrite($out, "\n");
		
	}else{
		
		$parts = explode("\t", $token);
		fwrite($out, $parts[0]);
		
		switch($parts[2]){
			case "location\n":
				fwrite($out, "|LOC ");
				break;
			case "person\n":
				fwrite($out, "|PERSON ");
				break;
			case "organization\n":
				fwrite($out, "|ORGANIZATION ");
				break;
			default:
				fwrite($out, " ");
		}
	}
}
fclose($in);
fclose($out);
