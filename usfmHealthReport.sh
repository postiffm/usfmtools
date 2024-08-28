#!/bin/bash
# 4/4/2024 add .SFC to accommodate Pemon file names
# Assumes you are in AndroidApps\usfm\<bible>\ or similar
../../usfmtools/findbadverseusfm.pl *.SFM *.usfm *.SFC > usfm.vreport
grep -s '\\r' *.SFM *.usfm *.sfm *.SFC > usfm.xrefreport
cat usfm.xrefreport |  ../../usfmtools/distillRefs.pl > usfm.distilledxrefreport
grep 'Number of total xrefs' usfm.distilledxrefreport
# Find all markers and annotate the "illegal" ones from BI's perspective
echo "Finding USFM markers...look in markers.txt"
python3 ../../usfmtools/findMarkers.py *.SFM *.usfm *.sfm *.SFC > markers.txt
# Get versification information from each translation
../../usfmtools/countChaptersVerses.py *.SFM *.usfm *.sfm *.SFC >& verseErrors.txt > verses.txt
