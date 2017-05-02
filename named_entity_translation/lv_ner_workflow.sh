#!/bin/bash

#The full workflow for NE tagging and post-processing Latvian texts
#Requires the input text file as the only parameter

#Path to LVTagger (https://github.com/PeterisP/LVTagger)
LVTagger_path="/home/user/LVTagger" 

$LVTagger_path/morphotagger.sh -conll-x < $1 > ./morphotagged.lv

java -mx1g -Xmx15360m -Dfile.encoding=utf-8 \
-cp "$LVTagger_path/dist/CRF.jar" edu.stanford.nlp.ie.crf.CRFClassifier -prop ./lv-ner-tag.prop \
> ./nertagged.lv

php tagToPipe.php ./nertagged.lv