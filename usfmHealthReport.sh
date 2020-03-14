#!/bin/bash

# Assumes you are in AndroidApps\usfm\<bible>\ or similar
../../usfmtools/findbadverseusfm.pl *.SFM *.usfm > usfm.vreport
grep '\\r' *.SFM *.usfm > usfm.xrefreport
grep '\\r' *.SFM *.usfm |  ~/bibledit-desktop/linux/distillRefs.pl > usfm.distilledxrefreport
grep 'Number of total xrefs' usfm.distilledxrefreport
