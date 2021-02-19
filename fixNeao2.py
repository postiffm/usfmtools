#!/usr/bin/python3
import os
import regex
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
    os.rename(file, filebak)

    # open the new .bak file for input; assume UTF-8 (USFM)
    fi = io.open(filebak, mode="r", encoding="utf-8", newline='')

    # prepare to write modified contents to the original filename
    fo = io.open(file, mode="w", encoding="utf-8", newline='')

    for cnt, line in enumerate(fi):
        #print("Working on " + line)
        # Round 5 Fixes
        if ("Klis," in line):
            line = regex.sub("Klis,", "Klisι", line)
        fo.write(line)

fi.close()
fo.close()
