#!/bin/bash

# For loop #1
for f in 'Akha' 'Bualkhaw Chin NT' 'Chakma NT' 'Chiru NT' 'Dagaara NT' 'Dagba NT' 'Darlong Bible' 'Day NT' 'Dendi NT' 'Falam Bible' 'Haitian Creole NT Ps Pr' 'Hakha Chin NT' 'Inner Seraji NT' 'Inpui Naga NT' 'Kabiye NT' 'Kaulong NT' 'Koyra Ciini Songhay' 'Lamkaang NT' 'Luxembourgish NT' 'Manipuri Bible' 'Mizo LUS NT' 'Sara Ngam NT' 'Quechua NT' 'Ranglong NT' 'Rito NT' 'Sango' 'Sara Kaba Deme Bible' 'Sara Kaba Naa NT' 'Sara Madjingaye Bible' 'Simte NT Ps Pv' 'Tenek' 'Tumak' 'Waali Bible' 'Warao Bible' 'Zarma Bible' 'Zokam NT' 'Zotung Chin NT'
do

# For loop #2...inside loop #1
for d in 'usfm_rev1' 'usfm_rev2' 'usfm_rev3' 'usfm_rev4' 'usfm_rev5' 'usfm_rev6'
do

# Generate USFM health report
if [ -e "$f/$d" ]
then
    cd "$f/$d"
    pwd
    ../../Scripts/usfmHealthReport.sh
    cd ../..
fi

# End for loop #2
done

# For loop #3...inside loop #1 (not #2)
for d in 'usfm_rev6' 'usfm_rev5' 'usfm_rev4' 'usfm_rev3' 'usfm_rev2' 'usfm_rev1'
do

# Check for missing \rq* markers in the usfm.xrefreport file generated above
if [ -e "$f/$d" ]
then
    cd "$f/$d"
    pwd
    grep '\\rq' usfm.xrefreport
     #| grep -v '\\rq*'
    cd ../..
    # Because I look at the latest version of usfm first, this saves us
    # irrelevant work.
    break
fi
    
# End for loop #3
done

# End for loop #1    
done
