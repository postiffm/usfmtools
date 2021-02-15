#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2021
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Explanation: See usfm\neao\README.txt notes from 1/16/2021 that show the 
# replacements that need to be made to correct the text.

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: fixNeao.py file [file ...]\n")
	exit(1)

script = sys.argv.pop(0)

for file in sys.argv:
    print("Processing " + file)
    filebak = file + ".bak"
    if os.path.isdir(file):
        print("Cannot process directory " + file + "\n")
        continue

    # rename the file to .bak
    #os.rename(file, filebak)

    # open the new .bak file for input; assume UTF-8 (USFM)
    fi = io.open(file, mode="r", encoding="utf-8", newline='')

    # prepare to write modified contents to the original filename
    #fo = io.open(file, mode="w", encoding="utf-8", newline='')

    for cnt, line in enumerate(fi):
        #print("Working on " + line)
        if ("ye ,an" in line):
            #print(f"Rule #1 in line {cnt}:{line}")
            line = re.sub("ye ,an", "ye ιan", line)
        if ("gbu ,an" in line):
            #print(f"Rule #2 in line {cnt}:{line}")
            line = re.sub("gbu ,an", "gbu ιan", line)
        if ("Klis,a" in line):
            #print(f"Rule #3 in line {cnt}:{line}")
            line = re.sub("Klis,a", "Klisιa", line)
        if (re.search("[0-9] ,a", line) != None):
            #print(f"Rule #4 in line {cnt}:{line}")
            line = re.sub("([0-9]) ,a", "\1 𝑙a", line)
        if (re.search("[\.\:] ,a", line) != None):
            #print(f"Rule #5 in line {cnt}:{line}")
            line = re.sub("([\.\:]) ,a", "\1 𝑙a", line)
        if (re.search("‑n,a", line) != None):
            #print(f"Rule #6.1 in line {cnt}:{line}")
            line = re.sub("‑n,a", "‑nιa", line)
        if (re.search("w,a", line) != None):
            #print(f"Rule #6.2 in line {cnt}:{line}")
            line = re.sub("w,a", "‑wιa", line)
        if (re.search("w,a,n", line) != None):
            #print(f"Rule #6.3 in line {cnt}:{line}")
            line = re.sub("w,a,n", "wιaιn", line)

        #fo.write(line)

fi.close()
#fo.close()
