#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2021
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Explanation: The word "úwa" (or Úwa) is used in some headings in Sara Kaba Naa
# and it means "cf." This does not work with Scripture App Builder
# very well and new BI style guide eliminates that. We have permission
# from Anna Beth Wivell to remove them in \r lines (not in the Bible text!)

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: removeUsaSKN.py file [file ...]\n")
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
        if ("\\r " in line):
            line = re.sub("Úwa ", "", line)
            line = re.sub("úwa ", "", line)
        fo.write(line)

fi.close()
fo.close()
