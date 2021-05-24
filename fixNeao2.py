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
            # This is the name of Christ, the comma should be an iota
            line = regex.sub("Klis,", "Klisι", line)
        if ("𝑙" in line):
            # Replace arithmetic small italic L U+1D459 with capital iota U+0399 (UTF-8 CE99)
            # which we believe corresponds to the lowercase iota U+03B9 (UTF-8 CEB9)
            # See subsequent email from Janet Austin 5/21/2021 which questions the above 
            # change. MAP is unsure what needs to be done. It appears that the capital Iota
            # is indistinguishable from the English capital I on the keyboard. Perhaps the font
            # will make it better.
            line = regex.sub("𝑙", "Ι", line) 
        if (regex.search(r"(\S),(\S)", line) != None):
            line = regex.sub(r"(\S),(\S)", r"\1ι\2", line)
        fo.write(line)

fi.close()
fo.close()
