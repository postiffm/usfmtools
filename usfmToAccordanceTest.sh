#!/bin/sh

# Run some test files and produce output to compare to known good

SCRIPT='python3 usfmToAccordance.py'

$SCRIPT test1.usfm > test1.acc
$SCRIPT test2.usfm > test2.acc
$SCRIPT test3.usfm > test3.acc
$SCRIPT test4.usfm > test4.acc
# Test if verse number is missing. Should say
# ERROR: Missing verse number in test5.usfm:3
$SCRIPT test5.usfm > test5.acc
# Test if chapter number is missing. Should say
# ERROR: Missing chapter number in test6.usfm:2
$SCRIPT test6.usfm > test6.acc
$SCRIPT test7.usfm > test7.acc
$SCRIPT test8.usfm > test8.acc
$SCRIPT test9.usfm > test9.acc
# Problem with simple footnotes - must eliminate
$SCRIPT test10.usfm > test10.acc
# Problem with complex glossary entries with strong number attributes must eliminate
$SCRIPT test11.usfm > test11.acc
# More problems with glossary \w and footnotes
$SCRIPT test12.usfm > test12.acc
