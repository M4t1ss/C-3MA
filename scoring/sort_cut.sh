#!/bin/bash

#Read from standard input
PPL_FILE=${1:-/dev/stdin} 

#How much is a half?
LINE_COUNT=`wc -l $PPL_FILE | awk '{print $1}'`
LINE_COUNT=$(($LINE_COUNT/2))

#Sort by second column and output the first column (only IDs) of the first half to standard output
sort -t$'\t' -nk2 $PPL_FILE | head -n $LINE_COUNT | awk '{print $1}'