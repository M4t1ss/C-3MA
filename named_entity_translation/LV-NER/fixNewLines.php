<?php
/*
Removes unnecessary new line symbols from the pipe delimited file 

Inputs:
	* The original non-tagged input file
	* The pipe delimited NER tagged file as inputs (produced by tagToPipe.php)
Outputs:
	* A .correct file with new line symbols just like in the original input
Example:
	php fixNewLines.php source.lv source.lv.pipe
*/

$goodF 	= $argv[1];
$badF 	= $argv[2];

$inG  = fopen($goodF, "r") or die("Can't open input file!");
$inB  = fopen($badF, "r") or die("Can't open input file!");
$out = fopen($badF.".correct", "a") or die("Can't create output file!");


while (($goodLine = fgets($inG)) !== false) {
	$badLine = fgets($inB);
	
	if(strcmp(cleanForChecking($goodLine), cleanForChecking($badLine)) == 0){
		fwrite($out, $badLine);
	}else{
		while(strcmp(cleanForChecking($goodLine), cleanForChecking($badLine)) != 0){
			$badNextLine = fgets($inB);
			$badLine = str_replace("\n", $badNextLine, $badLine);
		}
		fwrite($out, str_replace("\n", "", $badLine).$badNextLine);
	}
}

fclose($inG);
fclose($inB);
fclose($out);

function cleanForChecking($text){
	$text = str_replace("_", "", $text);
	$text = str_replace(" ", "", $text);
	$text = str_replace("\n", "", $text);
	$text = str_replace("|LOC", "", $text);
	$text = str_replace("|PERSON", "", $text);
	$text = str_replace("|ORGANIZATION", "", $text);
	$text = trim($text);
	
	return $text;
}