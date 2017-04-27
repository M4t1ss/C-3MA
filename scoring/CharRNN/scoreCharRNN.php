<?php
//Scores a file containing one sentence per line, using a CharRNN language model
//Outputs line number and perplexity score separated by one tab symbol for each sentence
//This is slower than "measure_file_perplexity.lua" - better use that instead!

//Input parameters
$source_sentences 	= $argv[1];
$language_model 	= $argv[2];

//Open files
$inSRC = fopen($source_sentences, "r") or die("Can't open input file!");
$output = fopen($source_sentences.".ppl.out", "a") or die("Can't create output file!");


$i = 1;
while (($sourceSentence = fgets($inSRC)) !== false) {
    $perplexity = shell_exec('./queryCharRNN.sh '.$language_model.' "'.$sourceSentence.'"');

    fwrite($output, $i . "\t" . $perplexity);

    $i++;
}