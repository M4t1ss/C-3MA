#!/bin/bash

#Measure perplexity of an input sentence, given a CharRNN language model

model_name=$1

DATA="$2"
sentence=`echo $DATA | sed -e '$a\'`

perplexity=`th measure_perplexity.lua -data_string "$sentence" $model_name | grep -e 'Perplexity per word' | sed -e 's/Perplexity per word: //g'`

echo $perplexity
