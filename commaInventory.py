#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, November 25, 2021
# Build a "comma inventory" from SFM. Originally designed for 
# the Neao...to see if we can find patterns that can be replaced to
# correct comma-should-be-iota.

if len(sys.argv) < 2:
	print(f"Usage: {sys.argv[0]} file [file ...]\n")
	exit(1)

script = sys.argv.pop(0)

# Empty dictionary that will store pairs of comma-strings and counts
# e.g. "x, ":5, "n, ":17, etc. 
d = {}

for file in sys.argv:
    print("Processing " + file)
    #filebak = file + ".bak"
    if os.path.isdir(file):
        print("Cannot process directory " + file + "\n")
        continue

    fi = io.open(file, mode="r", encoding="utf-8", newline='')

    for cnt, line in enumerate(fi):
        # Build dictionary for , and show chars before and after
        r = regex.findall(r".{0,1},.{0,1}", line)
        #print(r)
        for entry in r:
            if entry in d:
                d[entry] = d[entry]+1
            else:
                d[entry] = 1

for entry in d:
    newEntry = entry.replace("\r", '<CR>')
    print(f"'{newEntry}'\t{d[entry]}")

fi.close()
