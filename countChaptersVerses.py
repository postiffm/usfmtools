#!/usr/bin/python3

# (c) Matt Postiff, 2020
# This script counts finds the total verses in each chapter of the USFM
#
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'
# pip3 install regex

# Usage:
# countChaptersVerses.py testCountChaptersVerses.usfm

import copy
import click
import regex
from operator import itemgetter
import functools
import sys

# Dictionary for quick conversion of book names.
canonicalBookName = {
"GEN" : "Gen.",
"EXO" : "Ex.",
"LEV" : "Lev.",
"NUM" : "Num.",
"DEU" : "Deut.",
"JOS" : "Josh.",
"JDG" : "Judg.",
"RUT" : "Ruth",
"1SA" : "1Sam.",
"2SA" : "2Sam.",
"1KI" : "1Kings",
"2KI" : "2Kings",
"1CH" : "1Chr.",
"2CH" : "2Chr.",
"EZR" : "Ezra",
"NEH" : "Neh.",
"EST" : "Esth.",
"JOB" : "Job",
"PSA" : "Psa.",
"PRO" : "Prov.",
"ECC" : "Eccl.",
"SNG" : "Song",
"ISA" : "Is.",
"JER" : "Jer.",
"LAM" : "Lam.",
"EZK" : "Ezek.",
"DAN" : "Dan.",
"HOS" : "Hos.",
"JOL" : "Joel",
"AMO" : "Amos",
"OBA" : "Obad.",
"JON" : "Jonah",
"MIC" : "Mic.",
"NAM" : "Nah.",
"HAB" : "Hab.",
"ZEP" : "Zeph.",
"HAG" : "Hag.",
"ZEC" : "Zech.",
"MAL" : "Mal.",
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

DEBUG = 0
def debug(msg:str, lineEnd=''):
    if (DEBUG):
        print(msg) # end=lineEnd)

def error(msg:str):
    #print(f"ERROR: {msg}")
    sys.exit(f"ERROR: {msg}")

# Split words like justify\w* where there is no space before
# the usfm marker. Found that I also need to split for 
# punctuation: justify\w*, is a common scenario. 12/4/2020
# I found cases like this: \x*“Cuihhleiah  and  Mip 23:24\x*cule: 
# where the end marker causes the first word of the verse
# to be "eaten.""
# Returns a list of "splitted" components
def extraSplit(words:[]) -> []:
    debug("\n\nDEBUGA In extraSplit with " + '~'.join(words))
    output = []  # Final list of "tokens"/words/"pieces" of the text, in order
    for word in words:
        hold = ""  # holding space to build up tokens that were "too" split up
        debug("DEBUGB before add to final output: " + word)
        # Split the word on * and \ and see what we get
        # The idea is to take a string like \x*cule: and
        # ultimately split it into \x* and cule: but there 
        # are different combinations of possibilities
        subwords = regex.split('([\*\\\\])', word)
        debug("DEBUGC " + '~'.join(subwords))
        for subword in subwords:
            debug("DEBUGD token: " + subword)
            if (subword == ''):
                pass
            elif (subword == '\\'):
                hold = '\\'
            elif (subword == '*'):
                hold = hold + "*"
                debug(("DEBUGE        add to final output: " + hold))
                output.append(hold)
                hold = ""
            elif (hold != ""):
                # We are holding something like a \\ marker, so we have to add to it
                hold = hold + subword
                debug("DEBUGF hold: " + hold)
            else: # nothing special, just add it to our output list
                if (hold != ""): # We are "holding onto" something, so dump it
                    error("The hold should be empty; it has " + hold)
                    exit(1)
                debug(("DEBUGH        add to final output: " + subword))
                output.append(subword)
        if (hold != ""): # A straggler we need to output
            debug(("DEBUGI        add to final output: " + hold))
            output.append(hold)
    debug("DEBUGJ: " + '~'.join(output))
    return output

# Special flag to indicate a need to print the first line in a special way
justStarted = True

verseDict = {}

def countChaptersVerses(filename):
    """Scans the entire USFM and re-formats for Accordance"""
    # Modes that the usfm scanner is in (parsing mode)
    NORMAL = 0 # regular Bible text
    MARKER = 1 # USFM marker
    PREFIX = 2 # file header info
    GLOSSARY = 3 # within a \w ... \w* section
    mode = PREFIX
    newParagraph = False
    usfmCode = ""
    markerPattern = r'\\(\S+)'
    markerPatternCompiled = regex.compile(markerPattern) # looking for a usfm \marker
    global justStarted
    # The following markers are ones we just "delete" from the text because they are
    # glossary or formatting markers. NOTE: The next line of code is critical. If there
    # is a marker that I have not seen before, I may lose words from the original USFM
    # and verses can appear to be truncated. Watch out for this in the future.
    markersToIgnore = ['li', 'q1', 'q2', 'qt', 'm', 'w', 'pi', 'pi2', 'b', 'nb', 'mi']
    # The current word list
    wordlist = []
    file = open(filename,'r')
    debug(f"Processing file {filename}")
    for lineno, line in enumerate(file):
        # Ignore blank lines
        if not line.strip():
            continue;

        debug("DEBUG1: " + line)

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
                bookid = words.pop(0)
                # We don't process the glossary book
                if (bookid == "XXA" or bookid == "XXB" or bookid == "FRT" or bookid == "GLO" or 
                    bookid == "XXC" or bookid == "XXD" or bookid == "INT" or bookid == "BAK" or
                    bookid == "XXE" or bookid == "XXF" or bookid == "XXG"):
                    file.close()
                    return
                book = canonicalBookName[bookid]
            elif (word == "\\c"):
                if not words:
                    error(f"Missing chapter number in {filename}:{lineno}")
                chapter = words.pop(0)
                verse = 0 # restart verse numbering
                mode = NORMAL # move out of PREFIX mode
            elif (word == "\\v"):
                if not words:
                    error(f"Missing verse number in {filename}:{lineno}")
                verse = words.pop(0)
                # Verse numbers should be monotonically increasing by one every time from the previous one
                prevVerse = verseDict.get((book, chapter), 0)
                if ((int(prevVerse)+1) != int(verse)):
                    error(f"Verse number {verse} is out of sequence in {book} {chapter}, last verse was {prevVerse}")
                verseDict[(book, chapter)] = verse

    file.close()

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    for filename in files:
        countChaptersVerses(filename)
    print(verseDict)

if __name__ == '__main__':
    main()
