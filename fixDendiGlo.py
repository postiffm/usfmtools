#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, October 2021
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Explanation: Replace $o with ɔ and $e with ɛ

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: fixDendiGlo.py A9GLODEN.SFM\n")
	exit(1)

script = sys.argv.pop(0)

count7 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
        if (regex.search(r"\$o", line) != None):
            count = len(regex.findall(r"\$o", line))
            line = regex.sub(r"\$o", r"ɔ", line)
            count7[1] = count7[1] + count
        if (regex.search(r"\$e", line) != None):
            count = len(regex.findall(r"\$e", line))
            line = regex.sub(r"\$e", r"ɛ", line)
            count7[2] = count7[2] + count

        fo.write(line)

fi.close()
fo.close()

for i in range(1, len(count7)):
    print(f"Fixed rule {i} in {count7[i]} lines (maybe multiple times)")