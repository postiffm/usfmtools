#!/bin/bash

# ls -l | grep "drw" | wc -l
# presently (2/28/2021 shows 45 apps)

LOGFILE="../loopAppsReport.txt"
date > $LOGFILE

# For loop
for f in akha bim_e_2020.10.20 bualkhaw chakma chiru dagaara darlong day \
dendi falamchin haitiancreole hakhachin innerseraji inpuinaga kabiye kaowlu \
kaulong koyraciini lamkaang luxembourgish manipuri matuchin mizo neao paite \
quechua ranglong rathawi rawang rito sango sarakabademe sarakabanaa \
saramadjingaye sarangam simte tagalog taisun tangkhulnaga tenek tumak \
waali warao zokam zotung
do

cd $f
echo "Checking USFM health of $f"
echo "===================================" >> $LOGFILE
echo $f >> $LOGFILE
echo "===================================" >> $LOGFILE
../../usfmtools/usfmHealthReport.sh >> $LOGFILE
cat usfm.distilledxrefreport >> $LOGFILE
grep "This marker" markers.txt >> $LOGFILE
cd ..

done
# End for loop

# Run the following to find all markers that are suspect:
# find . -name markers.txt -exec grep "This marker" {} \;

# To find total cross references in each translation, do this:
# find . -name usfm.distilledxrefreport -exec grep -H "total xrefs" {} \; > totalxrefs.txt
