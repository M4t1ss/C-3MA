#!/bin/bash

#The full workflow for NE tagging and post-processing Latvian texts
#Inputs:
#	* The original non-tagged input file
#Outputs:
#	* morphotagged.lv 			- morphologically tagged file
#	* nertagged.lv 				- named entity tagged file
#	* nertagged.lv.pipe 		- pipe delimited named entity tagged file with broken new line count
#	* nertagged.lv.pipe.correct - the final pipe delimited named entity tagged file
#Example:
#	./lv_ner_workflow.sh source.lv

#Path to LVTagger (https://github.com/PeterisP/LVTagger)
LVTagger_path="/home/user/LVTagger" 

#Get a morphologically tagged file
$LVTagger_path/morphotagger.sh -conll-x < $1 > ./morphotagged.lv

#Tag named entities
java -mx1g -Xmx15360m -Dfile.encoding=utf-8 \
-cp "$LVTagger_path/dist/CRF.jar" edu.stanford.nlp.ie.crf.CRFClassifier -prop ./lv-ner-tag.prop \
> ./nertagged.lv

#Convert to the pipe format
php tagToPipe.php ./nertagged.lv

#Get rid of excess new lines created by the morphological tagger
php fixNewLines.php $1 ./nertagged.lv.pipe