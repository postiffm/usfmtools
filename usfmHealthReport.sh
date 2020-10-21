#!/bin/bash

# Assumes you are in AndroidApps\usfm\<bible>\ or similar
../../usfmtools/findbadverseusfm.pl *.SFM *.usfm > usfm.vreport
grep -s '\\r' *.SFM *.usfm > usfm.xrefreport
grep -s '\\r' *.SFM *.usfm |  ../../usfmtools/distillRefs.pl > usfm.distilledxrefreport
grep 'Number of total xrefs' usfm.distilledxrefreport
echo "Finding USFM markers...look in markers.txt"
python3 ../../usfmtools/findMarkers.py *.SFM *.usfm > markers.txt
