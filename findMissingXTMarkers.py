#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, 2020
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Find (\xt ...) and alert user when \xt* does not appear

script = 'findMissingXTMarkers.py'

# Usage: python3 <script> file.usfm

if len(sys.argv) < 2:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

script = sys.argv.pop(0)

for file in sys.argv:
    print("Processing " + file)
    if os.path.isdir(file):
        print("Cannot process directory " + file + "\n")
        continue

    fi = open(file, mode="r", newline='')

    xtpattern = regex.compile(r"\(\\xt ([^*]+)\)")

    for cnt, line in enumerate(fi):
        if (xtpattern.search(line) != None):
            print(f"[No \\xt* found:{cnt+1}] " + line, end='')
        
        # OK, I didn't expect the above to return anything because 
        # fixMissingXTMarkers.py had fixed all those cases. What 
        # I need to do is find all matches of xt and compare
        # to all matches of xt* in each line, and find the lines
        # where there is an imbalance.
        xts     = regex.findall(r"\\xt ", line)
        xtstars = regex.findall(r"\\xt\*", line)
        if (len(xts) != len(xtstars)):
            print(f"[Mismatched \\xt, \\xt* found:{cnt+1}] " + line, end='')

    fi.close()

# The end
