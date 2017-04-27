<?php

//Input parameters
$source_sentences 	= $argv[1];	//path to source sentence file
$target_sentences	= $argv[2];	//path to target sentence file
$sentence_num 		= $argv[3];	//path to file with sentence IDs
$action 			= $argv[4]; //0 - remove sentences with the given IDs; 1 - keep sentences with the given IDs

//Open files
$inSRC = fopen($source_sentences, "r") or die("Can't open input file!");
$inTRG = fopen($target_sentences, "r") or die("Can't open input file!");
$inNUM = fopen($sentence_num, "r") or die("Can't open input file!");
$outSRC = fopen($source_sentences.".cleaned", "a") or die("Can't create output file!");
$outTRG = fopen($target_sentences.".cleaned", "a") or die("Can't create output file!");

$LineNumbers = file($sentence_num);
foreach($LineNumbers as &$LineNumber) {
    $LineNumber = trim($LineNumber);
}


$i = 1;
while (($sourceSentence = fgets($inSRC)) !== false && ($targetSentence = fgets($inTRG)) !== false) {
    if(
		($action == 0 && !in_array($i, $LineNumbers)) || 
		($action == 1 && in_array($i, $LineNumbers))){
        fwrite($outSRC, $sourceSentence);
        fwrite($outTRG, $targetSentence);
    }
    $i++;
}