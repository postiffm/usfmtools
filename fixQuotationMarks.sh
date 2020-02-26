#!/bin/sh

# Replace <<, >>, <, and > with simple straight quotation marks

# Double quotation marks...must do first
replace 's/<</\"/g' *.usfm
mkdir bak1
mv *.bak bak1
replace 's/>>/\"/g' *.usfm
mkdir bak2
mv *.bak bak2

# Single quotation marks
replace 's/</\'"'"'/g' *.usfm
mkdir bak3
mv *.bak bak3
replace 's/>/\'"'"'/g' *.usfm
mkdir bak4
mv *.bak bak4

# The crazy '"'"' notation above is to handle escaping of the single-quote
# mark. See stackoverflow.com/questions/1250079/how-to-escape-single-quotes-within-single-quoted-strings


# Could improve by using smart quotes
# The below code almost works, but perl complains "Wide character output"
# so I need to get it smarter.

# The curved single quote characters are U+2018 left single quotation
# mark and U+2019 right single quotation mark; the curved double
# quotes are U+201C left double quotation mark and U+201D right double
# quotation mark.

# Double quotation marks...must do first
#replace 's/<</\N{U+201C}/g' *.usfm
#mkdir bak1
#mv *.bak bak1
#replace 's/>>/\N{U+201D}/g' *.usfm
#mkdir bak2
#mv *.bak bak2

# Single quotation marks
#replace 's/</\N{U+2018}/g' *.usfm
#mkdir bak3
#mv *.bak bak3
#replace 's/>/\N{U+2019}/g' *.usfm
#mkdir bak4
#mv *.bak bak4
