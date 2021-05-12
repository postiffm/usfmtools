#!/bin/bash

# Assumes you are in AndroidApps\usfm\<bible>\ or similar
../../usfmtools/findbadverseusfm.pl *.SFM *.usfm > usfm.vreport
grep -s '\\r' *.SFM *.usfm *.sfm > usfm.xrefreport
cat usfm.xrefreport |  ../../usfmtools/distillRefs.pl > usfm.distilledxrefreport
grep 'Number of total xrefs' usfm.distilledxrefreport
# Find all markers and annotate the "illegal" ones from BI's perspective
echo "Finding USFM markers...look in markers.txt"
python3 ../../usfmtools/findMarkers.py *.SFM *.usfm *.sfm > markers.txt
# Get versification information from each translation
../../usfmtools/countChaptersVerses.py *.SFM *.usfm *.sfm 2>verseErrors.txt > verses.txt
