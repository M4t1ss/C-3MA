<?php

//Input parameters
$input_file = $argv[1];

//Open files
$inFile 	= fopen($input_file, "r") or die("Can't open input file!");
$outFile 	= fopen($input_file.".out", "w") or die("Can't create output file!");

while (($sentence = fgets($inFile)) !== false) {
	$output_sentence = replace_repetitions($sentence);
    fwrite($outFile, $output_sentence);
}

fclose($outFile);
fclose($inFile);

function sortByLength($a,$b){
  if($a == $b) return 0;
  return (strlen($a) > strlen($b) ? -1 : 1);
} 

function replace_repetitions($str){
	
    //escape special chars
	$str = str_replace("&quot;", "quot-quot", $str);
	$str = str_replace("&amp;", "amp-amp", $str);
	$str = str_replace("&apos;", "apos-apos", $str);
	$str = str_replace("&#124;", "124-124", $str);
	$str = str_replace("&#91;", "91-91", $str);
	$str = str_replace("&#93;", "93-93", $str);
	$str = str_replace("&lt;", "lt-lt", $str);
	$str = str_replace("&gt;", "gt-gt", $str);

	$results = get_repetitions($str);
	$workaround = $results;
	usort($results,'sortByLength');
	
	while(count($results) > 0){
		$workaround = $results;
		foreach($results as $result){
			$str = str_replace(" ".$result." ".$result." ", " ".$result." ", $str);
			$str = str_replace("\n".$result." ".$result." ", "\n".$result." ", $str);
			$str = str_replace(" ".$result." ".$result."\n", " ".$result."\n", $str);
			$str = str_replace("\n".$result." ".$result."\n", "\n".$result."\n", $str);
		}
		$results = get_repetitions($str);
		usort($results,'sortByLength');
		if(count(array_diff($workaround, $results)) == 0)
			break;
	}
	
	$str = str_replace("quot-quot", "&quot;", $str);
	$str = str_replace("amp-amp", "&amp;", $str);
	$str = str_replace("apos-apos", "&apos;", $str);
	$str = str_replace("124-124", "&#124;", $str);
	$str = str_replace("91-91", "&#91;", $str);
	$str = str_replace("93-93", "&#93;", $str);
	$str = str_replace("lt-lt", "&lt;", $str);
	$str = str_replace("gt-gt", "&gt;", $str);
	
	return $str;
}

function get_repetitions($str){
	$found = str_word_count(strtolower($str),1);
	//get all words with occurance of more then 1
	$counts = array_count_values($found);
	$repeated = array_keys(array_filter($counts,function($a){return $a > 1;}));
	//begin results with the groups of 1 word.
	$results = $repeated;
	while($word = array_shift($found)){
		if(!in_array($word,$repeated)) continue;
		$additions = array();
		while($add = array_shift($found)){
			if(!in_array($add,$repeated)) break;
			$additions[] = $add;
			$count = preg_match_all('/'.preg_quote($word).'\W+'.implode('\W+',$additions).'/si',$str,$matches);
			if($count > 1){
				$newmatch = $word.' '.implode(' ',$additions);
				if(!in_array($newmatch,$results)) $results[] = $newmatch;
			} else {
				break;
			}
		}
		if(!empty($additions)) array_splice($found,0,0,$additions);
	}
	return $results;
}