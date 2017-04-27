#!/bin/bash

#Track the perplexity improvement progress while training a language model

model_name=$1

latest_save=`ls cv -1t | head -n 1`
save_progress=`echo $latest_save | sed -e 's/lm_$model_name_epoch//g' | sed -e 's/.t7//g'`
epoch=`echo $save_progress | awk -F'_' '{print $1}'`
loss=`echo $save_progress | awk -F'_' '{print $2}'`

perplexity=`th measure_perplexity.lua -data_path /home/ubuntu/data/test.txt cv/$latest_save | grep -e 'Perplexity per word' | sed -e 's/Perplexity per word: //g'`


echo "Epoch"$'\t'"Loss"$'\t'"Perplexity"
echo "$epoch"$'\t'"$loss"$'\t'"$perplexity"

echo "$epoch"$'\t'"$loss"$'\t'"$perplexity" >> progress_$model_name.txt