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

count6 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

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
        # Round 6 Fixes
        # 6.1 - Fixed by hand ´w,, to ´wι,
        count6[1] = 1
        # 6.2 ´w,,,n‑´ all three , to iota
        if (regex.search(r"´w,,,n‑´", line) != None):
            line = regex.sub(r"´w,,,n‑´", r"´wιιιn‑´", line)
            count6[2] = count6[2] + 1
        if (regex.search(r"´w,,n", line) != None):
            line = regex.sub(r"´w,,n", r"´wιιn", line)
            count6[3] = count6[3] + 1
        if (regex.search(r"´w,", line) != None):
            line = regex.sub(r"´w,", r"´wι", line)
            count6[4] = count6[4] + 1
        if (regex.search(r"´W,kpɔ", line) != None):
            line = regex.sub(r"´W,kpɔ", r"´Wιkpɔ", line) # Note capital W not handled above
            count6[6] = count6[6] + 1  # Yes, it is SIX, not FIVE. 5 is subsumed inside of 4
        if (regex.search(r"´W,a", line) != None):
            line = regex.sub(r"´W,a", r"´Wιa", line) # Note capital W not handled above
            count6[12] = count6[12] + 1  # Yes, it is 12

        fo.write(line)

fi.close()
fo.close()

for i in range(1, len(count6)):
    print(f"Fixed rule {i} {count6[i]} times")