#!/bin/bash

# ls -l | grep "drw" | wc -l
# presently (10/26/2021 shows 48 apps)

LOGFILE="loopAppsReport.txt"
date > $LOGFILE
# Slight change so log file is addressed correctly in the loop below
LOGFILE="../loopAppsReport.txt"

# For loop
# I have omitted bimodel here because it has three sets of USFM in it
# and that messes up verse checks.
for f in akha bualkhaw chakma chiru dagaara dagba darlong day \
dendi falamchin haitiancreole hakhachin innerseraji inpuinaga kabiye kaowlu \
kaulong koyraciini lamkaang luxembourgish manipuri matuchin mizo neao paite \
quechua ranglong rathawi rawang rito sango sarakabademe sarakabanaa \
saramadjingaye sarangam simte tagalog taisun tangkhulnaga tenek tumak \
waali warao zarma zokam zotung mbur
do

cd $f
echo "Checking USFM health of $f"
echo "===================================" >> $LOGFILE
echo "Translation for language $f" >> $LOGFILE
echo "===================================" >> $LOGFILE
../../usfmtools/usfmHealthReport.sh >> $LOGFILE
cat usfm.distilledxrefreport >> $LOGFILE
grep "This marker" markers.txt >> $LOGFILE
cat verseErrors.txt >> $LOGFILE
git status >> $LOGFILE
cd ..

done
# End for loop

# Run the following to list all markers that are suspect with filenames:
# find . -name markers.txt -exec grep -H "This marker" {} \;

# Run the following to find all markers that are suspect:
# find . -name markers.txt -exec grep "This marker" {} \; | ../usfmtools/sumBadMarkers.pl > badmarkers.txt

# To find total cross references in each translation, do this:
# find . -name usfm.distilledxrefreport -exec grep -H "total xrefs" {} \; > totalxrefs.txt

# To gather all cross references in the  translations, do this:
# find . -name usfm.xrefreport -exec cat {} \; > allxrefs.txt

# To find all versification errors in the translations, do this:
# find . -name verseErrors.txt -exec grep -H "ERROR" {} \; > allVerseErrors.txt
