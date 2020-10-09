#!/usr/bin/python3

# (c) Matt Postiff, 2020
# This script converts USFM into an Accordance-compliant (very simplified) text file
#
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'
# pip3 install regex

# Usage:
# python3 usfmToAccordance.py test1.usfm > test1.txt

import copy
import click
#import re
import regex
from operator import itemgetter
import functools

# Find all phrases of length=sequencelength, repeated more than once, from in_file
def convertUSFMToAccordance(filename):
    """Scans the entire USFM and re-formats for Accordance"""
    # Modes that the usfm scanner is in (parsing mode)
    NORMAL = 0 # regular Bible text
    MARKER = 1 # USFM marker
    PREFIX = 2 # file header info
    mode = PREFIX
    usfmCode = ""
    markerPattern = r'\\(\S+)'
    markerPatternCompiled = regex.compile(markerPattern) # looking for a usfm \marker
    markersToIgnore = ['li', 'q1', 'm']
    # The current word list
    wordlist = []
    file = open(filename,'r')
    print(f"Processing file {filename}")
    for line in file:
        # Ignore blank lines
        if not line.strip():
            continue;

        #print("DEBUG1: " + line, end='')

        # Disregard line/verse boundaries so that repeats can cross lines/verses
        words = line.split()

        # Handle USFM codes (by noting them or dropping them)
        while words:
            word = words.pop(0)
            markerMatch = markerPatternCompiled.match(word)
            #print("DEBUG2: " + "Word=" + word + " " + ' '.join(words))
            # Capture context of book chapter:verse
            if (word == "\\id"):
                book = words.pop(0)
                #print(f"Found book {book}")
            elif (word == "\\c"):
                chapter = words.pop(0)
                #print(f"Found chapter {chapter}")
            elif (word == "\\v"):
                verse = words.pop(0)
                #print(f"Found verse {verse}")
                print(f"OUTPUT: {book} {chapter}:{verse} ", end='')
                mode = NORMAL
            elif (markerMatch != None): # word is a USFM marker
                usfmCode = markerMatch.group(1)
                if (usfmCode.endswith('*')): # end marker
                    print(f"Found endmarker \{usfmCode} in {word}")
                    mode = NORMAL
                elif (usfmCode in markersToIgnore): # formatting markers like \li, q1
                    print(f"Found to-ignore marker \{usfmCode} in {word}")
                    mode = NORMAL
                else:
                    print(f"Found regular marker \{usfmCode} in {word}")
                    mode = MARKER
            elif (mode == NORMAL):
                # The fall-through case is simply to print the word
                print(word + " " , end='')
            
    # Close the file
    file.close()

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    for filename in files:
        convertUSFMToAccordance(filename)

if __name__ == '__main__':
    main()
