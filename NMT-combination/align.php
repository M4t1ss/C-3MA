<?php
error_reporting(E_ERROR);

//Input parameters - 3 .js files that are created by process_alignments.py from https://github.com/M4t1ss/SoftAlignments
$alignments = $argv[1];
$sources 	= $argv[2];
$targets 	= $argv[3];

$count = getLineCount($alignments)-3;
$sentence = 1;

//Load only the one line from each input file
$f1 = new SplFileObject($alignments);
$f2 = new SplFileObject($sources);
$f3 = new SplFileObject($targets);
$outFile 	= fopen($alignments.".maxAli", "w") or die("Can't create output file!");

for($i = 1; $i < $count; $i++){
	//The line of the sentence
	$f1->seek($i);
	$f2->seek($i);
	$f3->seek($i);

	$aliLine = $f1->current();
	$srcLine = $f2->current();
	$trgLine = $f3->current();

	//Arrays of source and target subword units
	$srcSubwords = getTokensFromJs($srcLine);
	$trgSubwords = getTokensFromJs($trgLine);
	//Array of alignments - sourceID, weight, targetID
	$aliSubwords = getAlignmentsFromJs($aliLine);

	$weightSums = array();

	foreach($aliSubwords as $aliSubword){
		$aliSubwordParts = explode(", ", $aliSubword);
		$weightSums[$aliSubwordParts[0]] += $aliSubwordParts[1];
	}
	$highestWeightSum = max($weightSums);
	$highestWeightID = array_keys($weightSums, max($weightSums))[0];
	//Writes sentence ID, number of subword units, subword unit ID with highest alignment weights, the highest alignment weights, final unit alignment weights
    fwrite($outFile, $i."\t".count($srcSubwords)."\t".$highestWeightID."\t".$highestWeightSum."\t".$weightSums[count($weightSums)-1]."\n");
}

fclose($outFile);

function getAlignmentsFromJs($string){
	$string = str_replace("], ], \n", "", $string);
	$string = str_replace("[[", "", $string);
	$tokenArray = explode('], [', $string);
	return $tokenArray;
}

function getTokensFromJs($string){
	$string = str_replace("], \n", "", $string);
	$string = str_replace("[", "", $string);
	$string = ltrim($string, '"');
	$string = rtrim($string, '"');
	$tokenArray = explode('", "', $string);
	return $tokenArray;
}

function getLineCount($fileName){
	$linecount = 0;
	$handle = fopen($fileName, "r");
	while(!feof($handle)){
	  $line = fgets($handle);
	  $linecount++;
	}
	fclose($handle);
	return $linecount;
}
