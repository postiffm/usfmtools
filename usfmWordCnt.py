#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, 2020
# This script counts words in the USFM. The results are a 
# dictionary that is printed.

# Usage: python3 usfmWordCnt.py *.SFM

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

# The dictionary that we are building...the main goal of this code
# It is augmented in the learnWord function
wordCntDict = {}

DEBUG = 0
def debug(msg:str, lineEnd=''):
    if (DEBUG):
        print(msg) # end=lineEnd)

def error(msg:str):
    print(f"ERROR: {msg}")

def learnWord(wrd:str):
    debug((f"Examining {wrd}, whose last char is {wrd[-1]}"))
    # Remove trailing , or .
    # Notice to match period, you use r".", not "\."
    if ((wrd[-1] == r".") or (wrd[-1] == r',')):
        debug(f"Removing last char of {wrd}")
        wrd = wrd[:-1]
        if (len(wrd) == 0):
            return

    if (wrd[0] == '\\'):
        # We have a USFM code. Ignore it.
        debug(f"Ignoring USFM marker: {wrd}")
        return
    elif (regex.search("[0-9]+:[0-9]+", wrd)):
        debug(f"Ignoring verse range: {wrd}")
    elif (regex.search("[0-9]+-[0-9]+", wrd)):
        debug(f"Ignoring numerical range: {wrd}")
    elif (regex.search("^[0-9]+$", wrd)):
        debug(f"Ignoring verse number or similar: {wrd}")
    else:
        if wrd in wordCntDict:
            wordCntDict[wrd] = wordCntDict[wrd]+1
        else:
            wordCntDict[wrd] = 1
            debug(f"Counted {wrd}")

def learnLine(line:str):
    debug(f"LINE: {line}")

    words = line.split()
    for i in range(0, len(words)):
        learnWord(words[i])
    return

for file in sys.argv:
    debug("Processing " + file)
    if os.path.isdir(file):
        error("Cannot process directory " + file + "\n")
        continue

    fi = open(file, mode="r", newline='')

    for cnt, line in enumerate(fi):
            learnLine(line)

    fi.close()

for o in wordCntDict:
    print(f"'{o}' : '{wordCntDict[o]}',")

# The end
