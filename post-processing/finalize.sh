#/bin/bash
#Remove repeated phrases, detruecase, detokenize, normalize punctuation and convert to sgm

file=./test/test.out.100

src=en
trg=lv

cat $file.$trg | \
php ./repeat.php | \
./detruecase.perl | \
./detokenizer.perl -l $trg | \
./normalize-punctuation.perl $trg | \
./wrap-xml.perl $trg ./test/newstest2017-$src$trg-src.$src.sgm C-3MA > $file.$trg.sgm


src=lv
trg=en

cat $file.$trg | \
php ./repeat.php | \
./detruecase.perl | \
./detokenizer.perl -l $trg | \
./normalize-punctuation.perl $trg | \
./wrap-xml.perl $trg ./test/newstest2017-$src$trg-src.$src.sgm C-3MA > $file.$trg.sgm

