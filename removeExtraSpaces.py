#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, 2022
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Hunting for space-space or similar and remove from the USFM

# To do:
# Fix error handling. If .bak file already exists, do something smart.

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print("Usage: {script} file [file ...]\n")
    exit(1)

# Count number of lines of USFM changed
numLines = 0;

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
        if (regex.search('  ', line)):
            #print("  Found two spaces")
            numLines += 1
            line = regex.sub('  ', ' ', line, count=0)
        if (regex.search("[\d]:\s[\d]", line)):
            #print("  Found digit:<space>digit")
            numLines += 1
            line = regex.sub("([\d]):\s([\d])", r'\1:\2', line, count=0)
        fo.write(line)

    fi.close()
    fo.close()

print (f"    Changed {numLines} lines of USFM")
