# Find sentences that contain UNKs and Latvian diacritics
echo "UNKs and Latvian diacritics:"
grep -Eic "\<unk\>|ā|ē|ī|ū|ķ|ļ|ņ|ģ|š|ķ" $1
grep -Ein "\<unk\>|ā|ē|ī|ū|ķ|ļ|ņ|ģ|š|ķ" $1 | cut -f1 -d: > $1.all.num.txt

# Find only sentences that contain UNKs
echo "Only UNKs:"
grep -Eic "\<unk\>" $1
grep -Ein "\<unk\>" $1 | cut -f1 -d: > $1.unk.num.txt

