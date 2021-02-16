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
        # Round 1 Fixes
        if ("ye ,an" in line):
            #print(f"Rule #1 in line {cnt}:{line}")
            # The special character ι is the Greek Iota,
            # U+O399, UTF-8 CE 99
            line = regex.sub("ye ,an", "ye ιan", line)
        if ("gbu ,an" in line):
            #print(f"Rule #2 in line {cnt}:{line}")
            line = regex.sub("gbu ,an", "gbu ιan", line)
        if ("Klis,a" in line):
            #print(f"Rule #3 in line {cnt}:{line}")
            line = regex.sub("Klis,a", "Klisιa", line)
        if (regex.search("[0-9] ,a", line) != None):
            #print(f"Rule #4 in line {cnt}:{line}")
            # The special character 𝑙 is like an italics L, 
            # technically Mathematical Italic Small L, U+1D459
            # UTF-8 0xF0 0x9D 0x91 0x99
            line = regex.sub(r"([0-9]) ,a", r"\1 𝑙a", line)
        if (regex.search("[\.\:] ,a", line) != None):
            #print(f"Rule #5 in line {cnt}:{line}")
            line = regex.sub(r"([\.\:]) ,a", r"\1 𝑙a", line)
        if (regex.search(r"‑n,a", line) != None):
            #print(f"Rule #6.1 in line {cnt}:{line}")
            line = regex.sub(r"‑n,a", r"‑nιa", line)
        if (regex.search("w,a", line) != None):
            #print(f"Rule #6.2 in line {cnt}:{line}")
            line = regex.sub("w,a", "wιa", line)
        if (regex.search("wιa,n", line) != None):
            # Originally this rule said w,a,n, but the code
            # just above changes the first part so the match 
            # won't occur.
            #print(f"Rule #6.3 in line {cnt}:{line}")
            line = regex.sub("wιa,n", "wιaιn", line)
        # Round 2 Fixes
        if (" ,an" in line):
            line = regex.sub(" ,an", " 𝑙an", line)
        if (" ,n" in line):
            line = regex.sub(" ,n", " 𝑙a", line)
        # Round 3 Fixes
        if (" ‑n,." in line):
            line = regex.sub(r" ‑n,\.", r" -nι.", line)
        if (" ‑n," in line):
            line = regex.sub(" ‑n,", " -nι", line)
        if (" n,," in line):
            line = regex.sub(" n,,", " nι-,", line)
        if (" n," in line):
            line = regex.sub(" n,", " nι", line)
        if (" d," in line):
            line = regex.sub(" d,", " dι", line)
        if (" kp,n" in line):
            line = regex.sub(" kp,n", " kpιn", line)
        if (" kp,ɔn" in line):
            line = regex.sub(" kp,ɔn", " kpιɔn", line)
        # Round 4 Fixes
        if (" : " in line):  # should be capital Ɔ
            line = regex.sub(" : ", " Ɔ ", line)
        fo.write(line)

fi.close()
fo.close()
