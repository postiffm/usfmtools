#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, June 2021
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Explanation: Replace fix all word-medial commas and change them to ι
# Also space-,-space should be an iota as well. 
# Also  if comma ocurs at beginning of a word or after tone marking, change it
# to iota. I don't know what tone markings are.
# Also fix :ɔ to Ɔɔ

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: fixNeao4.py file [file ...]\n")
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
        # Round 7 Fixes
        # 7.1 Fix comma , in the middle of a word, change over to ι
        if (regex.search(r"[\S],[\S]", line) != None):
            line = regex.sub(r"([\S]),([\S])", r"\1ι\2", line)
            count7[1] = count7[1] + 1
        if (regex.search(r"[\s],[\s]", line) != None):
            line = regex.sub(r"([\s]),([\s])", r"\1ι\2", line)
            count7[2] = count7[2] + 1
        if (regex.search(r"[\s],[\S]", line) != None):
            line = regex.sub(r"([\s]),([\S])", r"\1ι\2", line)
            count7[3] = count7[3] + 1
        if (regex.search(r":ɔ", line) != None):
            line = regex.sub(r":ɔ", r"Ɔɔ", line)
            count7[4] = count7[4] + 1

        fo.write(line)

fi.close()
fo.close()

for i in range(1, len(count7)):
    print(f"Fixed rule {i} {count7[i]} times")