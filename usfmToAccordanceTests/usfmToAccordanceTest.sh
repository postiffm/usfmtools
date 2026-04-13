#!/bin/sh -v

# Run some test files and produce output to compare to known good

SCRIPT='python3 ../usfmToAccordance.py'

$SCRIPT test1.usfm > test1.tmp
diff test1.acc test1.tmp
$SCRIPT test2.usfm > test2.tmp
diff test2.acc test2.tmp
$SCRIPT test3.usfm > test3.tmp
diff test3.acc test3.tmp
$SCRIPT test4.usfm > test4.tmp
diff test4.acc test4.tmp
# Test if verse number is missing. Should say
# ERROR: Missing verse number in test5.usfm:3
$SCRIPT test5.usfm > test5.tmp
diff test5.acc test5.tmp
# Test if chapter number is missing. Should say
# ERROR: Missing chapter number in test6.usfm:2
$SCRIPT test6.usfm > test6.tmp
diff test6.acc test6.tmp
$SCRIPT test7.usfm > test7.tmp
diff test7.acc test7.tmp
$SCRIPT test8.usfm > test8.tmp
diff test8.acc test8.tmp
$SCRIPT test9.usfm > test9.tmp
diff test9.acc test9.tmp
# Problem with simple footnotes - must eliminate
$SCRIPT test10.usfm > test10.tmp
diff test10.acc test10.tmp
# Problem with complex glossary entries with strong number attributes must eliminate
$SCRIPT test11.usfm > test11.tmp
diff test11.acc test11.tmp
# More problems with glossary \w and footnotes
$SCRIPT test12.usfm > test12.tmp
diff test12.acc test12.tmp
$SCRIPT test13.usfm > test13.tmp
diff test13.acc test13.tmp
