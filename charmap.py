#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# Take one or more text files and build a character map from it

# Usage: python3 charmap.py learn.txt

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

charDict = {}

def charmap(txt:str):
    # Count all the different characters in a string
    for c in txt:
        cnt = charDict.get(c, 0)
        charDict[c] = cnt+1

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
            charmap(line)

    fi.close()

for c in charDict:
#    if (c == "\n"):
#        cToPrint = "\\n"
#    elif (c == "\r"):
#        cToPrint = "\\r"
#    elif (c == " "):
#        cToPrint = "<spc>"
#    else:
    cToPrint = c;
    print(f"'{cToPrint}'  :  '{charDict[c]}',")

# The end
