#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2021
# Find all glossary entries in given USFM that 
# have multiple words. Example:
# \p \k Alpha at Omega\k* Ang una...

# Usage: findMultiWordGloEntries.py A9GLOTNT20.SFM

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

DEBUG = 1
def debug(msg:str, lineEnd=''):
    if (DEBUG):
        print(msg) # end=lineEnd)

def error(msg:str):
    print(f"ERROR: {msg}")

for file in sys.argv:
    debug("Processing " + file)
    if os.path.isdir(file):
        error("Cannot process directory " + file + "\n")
        continue

    fi = open(file, mode="r", newline='')

    for cnt, line in enumerate(fi):
        segments = line.split("\k", )
        #print(segments)
        if (len(segments) > 1):
            #print(f"Found more than one segment; must have been a \k present")
            keyword = segments[1]
            print(f"Keyword = {keyword}", end='')
            if (keyword[0] == " "): 
                # Delete the initial space
                keyword = keyword[1:]
            if (" " in keyword):
                print(" <== There is a space in this keyword!")
            else:
                print("")
    fi.close()

# The end
