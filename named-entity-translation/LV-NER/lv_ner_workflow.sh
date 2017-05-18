#!/bin/bash

#The full workflow for NE tagging and post-processing Latvian texts
#Inputs:
#	* The original non-tagged input file
#Outputs:
#	* morphotagged.lv 			- morphologically tagged file
#	* nertagged.lv 				- named entity tagged file
#	* nertagged.lv.pipe 		- pipe delimited named entity tagged file with broken new line count
#	* nertagged.lv.pipe.us 		- the final pipe delimited named entity tagged file
#Example:
#	./lv_ner_workflow.sh source.lv

#Path to LVTagger (https://github.com/PeterisP/LVTagger) & Moses Decoder
LVTagger_path="/data/matiss/tools/gh/LVTagger" 
mosesdecoder="/opt/bin/mosesdecoder/"

#Detruecase, detokenize and get a morphologically tagged file
cat $1 | \
$mosesdecoder/scripts/recaser/detruecase.perl | \
$mosesdecoder/scripts/tokenizer/detokenizer.perl -l lv > ./truecased.lv

$LVTagger_path/morphotagger.sh -conll-x < ./truecased.lv > ./morphotagged.lv

#Tag named entities
java -mx1g -Xmx15360m -Dfile.encoding=utf-8 \
-cp "$LVTagger_path/dist/CRF.jar" edu.stanford.nlp.ie.crf.CRFClassifier -prop ./lv-ner-tag.prop \
> ./nertagged.lv

#Convert to the pipe format
php tagToPipe.php ./nertagged.lv

#Get rid of excess new lines created by the morphological tagger
php fixLinesUnderscores.php ./truecased.lv ./nertagged.lv.pipe

$mosesdecoder/scripts/tokenizer/detokenizer.perl -l lv < ./nertagged.lv.pipe > ./final.nertagged.pipe.lv