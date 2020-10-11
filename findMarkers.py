#!/usr/bin/python3

# (c) Matt Postiff, 2020
# This script lists all USFM markers found in the text.
#
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'
# pip3 install regex

# Usage:
# python3 findMarkers.py test1.usfm

import copy
import click
#import re
import regex
from operator import itemgetter
import functools

def findUSFMMarkers(filename):
    """Scans the entire USFM and finds markers"""
    markerDB = {}
    usfmCode = ""
    markerPattern = r'\\([a-zA-Z0-9]+\*{0,1})'
    markerPatternCompiled = regex.compile(markerPattern) # looking for a usfm \marker

    wordlist = []
    file = open(filename,'r')
    print(f"Processing file {filename}")
    for line in file:
        # Ignore blank lines
        if not line.strip():
            continue;

        words = line.split()
        # Some words have usfm codes abutted to them with no space: justify\w*
        # So we need to split those apart before proceeding below.
        #words = extraSplit(words)

        # Handle USFM codes (by noting them or dropping them)
        while words:
            word = words.pop(0)
            #print(word)
            #markerMatch = markerPatternCompiled.search(word)
            #if (markerMatch != None): # word is a USFM marker
            for markerMatch in regex.finditer(markerPatternCompiled, word):
                usfmCode = markerMatch.group(1)
                #print(f"Marker {usfmCode}")
                count = markerDB.get(usfmCode, 0)
                markerDB[usfmCode] = count + 1;
            
    # Close the file
    file.close()

    for marker in markerDB:
        print(f"{marker}\t{markerDB[marker]}")

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    for filename in files:
        findUSFMMarkers(filename)

if __name__ == '__main__':
    main()
