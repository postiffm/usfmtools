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

# Dictionary for quick conversion of book names.
canonicalBookName = {
"MAT" : "Matt.",
"MRK" : "Mark",
"LUK" : "Luke",
"JHN" : "John",
"ACT" : "Acts",
"ROM" : "Rom.",
"1CO" : "1Cor.",
"2CO" : "2Cor.",
"GAL" : "Gal.",
"EPH" : "Eph.",
"PHP" : "Phil.",
"COL" : "Col.",
"1TH" : "1Th.",
"2TH" : "2Th.",
"1TI" : "1Tim.",
"2TI" : "2Tim.",
"TIT" : "Titus",
"PHM" : "Philem.",
"HEB" : "Heb.",
"JAS" : "James",
"1PE" : "1Pet.",
"2PE" : "2Pet.",
"1JN" : "1John",
"2JN" : "2John",
"3JN" : "3John",
"JUD" : "Jude",
"REV" : "Rev.",
}

# Split words like justify\w* where there is no space before
# the usfm marker. Found that I also need to split for 
# punctuation: justify\w*, is a common scenario. Returns 
# a list of "splitted" components
def extraSplit(words:[]) -> []:
    #print("DEBUG3: In extraSplit with " + ' '.join(words))
    output = []
    for word in words:
        #print("DEBUG5: " + word)
        delim = '\\'
        if delim in word:
            #print("DEBUG4: Found " + word)
            subwords = word.split(delim)
            subwords[-1] = delim + subwords[-1]
            # If you split "\v" on '\' you get subwords = ['', '\\v']
            if (subwords[0] == ''):
                subwords.pop(0)
            # Handle punctuation after a USFM marker
            if (subwords[-1].endswith(('.', ',', ';', ':'))):
                lastchar = subwords[-1][-1]
                subwords[-1] = subwords[-1][:-1] # remove last char
                subwords.append(str(lastchar)) # add last char as a new subword
            #print(subwords)
            output.extend(subwords)
        else:
            output.append(word)

    return output

# Special flag to indicate a need to print the first line in a special way
justStarted = True

# Find all phrases of length=sequencelength, repeated more than once, from in_file
def convertUSFMToAccordance(filename):
    """Scans the entire USFM and re-formats for Accordance"""
    # Modes that the usfm scanner is in (parsing mode)
    NORMAL = 0 # regular Bible text
    MARKER = 1 # USFM marker
    PREFIX = 2 # file header info
    mode = PREFIX
    newParagraph = False
    usfmCode = ""
    markerPattern = r'\\(\S+)'
    markerPatternCompiled = regex.compile(markerPattern) # looking for a usfm \marker
    global justStarted
    # The following markers are ones we just "delete" from the text because they are
    # glossary or formatting markers.
    markersToIgnore = ['li', 'q1', 'q2', 'm', 'w', 'pi', 'pi2', 'b', 'nb']
    # The current word list
    wordlist = []
    file = open(filename,'r')
    #print(f"Processing file {filename}")
    for line in file:
        # Ignore blank lines
        if not line.strip():
            continue;

        #print("DEBUG1: " + line, end='')

        # Disregard line/verse boundaries so that repeats can cross lines/verses
        words = line.split()
        # Some words have usfm codes abutted to them with no space: justify\w*
        # So we need to split those apart before proceeding below.
        words = extraSplit(words)

        # Handle USFM codes (by noting them or dropping them)
        while words:
            word = words.pop(0)
            markerMatch = markerPatternCompiled.search(word)
            #print("DEBUG2: " + "Word=" + word + " " + ' '.join(words))
            # Capture context of book chapter:verse
            if (word == "\\id"):
                book = canonicalBookName[words.pop(0)]
            elif (word == "\\c"):
                chapter = words.pop(0)
            elif (word == "\\v"):
                verse = words.pop(0)
                if (justStarted == False):
                    print(f"\n{book} {chapter}:{verse}", end='')
                else:
                    print(f"{book} {chapter}:{verse}", end='')
                    justStarted = False
                if (newParagraph == True):
                    print(" ¶", end='')
                    newParagraph = False # reset
                mode = NORMAL
            # Capture whether we are starting a new paragraph...for future use
            elif (word == "\\p"):
                newParagraph = True
            elif (markerMatch != None): # word is a USFM marker
                usfmCode = markerMatch.group(1)
                if ('*' in usfmCode): # end marker
                    #print(f"Found endmarker \{usfmCode} in {word}")
                    mode = NORMAL
                elif (usfmCode in markersToIgnore): # formatting markers like \li, q1
                    #print(f"Found to-ignore marker \{usfmCode} in {word}")
                    mode = NORMAL
                else:
                    #print(f"Found regular marker \{usfmCode} in {word}")
                    mode = MARKER
            elif (mode == NORMAL):
                # The fall-through case is simply to print the word
                # but if the "word" is just a punctuation marker, we don't 
                # want to put a space before it! But some words have
                # punctuation already, so we cannot simply look at the last
                # character
                if (word == '.' or word == ',' or word == ';' or word == ':'):
                    print(word, end='');
                else:
                    print(" " + word, end='')
            
    # Close the file
    file.close()

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    for filename in files:
        convertUSFMToAccordance(filename)

if __name__ == '__main__':
    main()
