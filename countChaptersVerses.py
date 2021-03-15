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
#from operator import itemgetter
import functools
import sys
import os
import pickle # for serializing dictionary to a file

DEBUG = False
def debug(msg:str, lineEnd=''):
    if (DEBUG):
        print(msg) # end=lineEnd)

def error(msg:str):
    #print(f"ERROR: {msg}")
    #sys.exit(f"ERROR: {msg}")
    # Do not stop in case of this error so that user can see all errors easily at one run
    sys.stderr.write(f"ERROR: {msg}\n")

verseDict = {}

# For saving and restoring the above verse dictionary to a file
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

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
    # The following markers are ones we just "delete" from the text because they are
    # glossary or formatting markers. NOTE: The next line of code is critical. If there
    # is a marker that I have not seen before, I may lose words from the original USFM
    # and verses can appear to be truncated. Watch out for this in the future.
    markersToIgnore = ['li', 'q1', 'q2', 'qt', 'm', 'w', 'pi', 'pi2', 'b', 'nb', 'mi']
    # The current word list
    wordlist = []
    try:
        # If you do not have utf_8_sig, the byte-order-mark ef bb bf messes up
        # the initial \id line so it does not match \\id below. This decoding
        # method dumps the BOM if it is present.
        file = open(filename, 'r', encoding='utf_8_sig')
    except IOError:
        # File does not exist...ignore...lets us pass wrong parameters like *.sfm *.usfm *.SFM and not worry
        return
    debug(f"Processing file {filename}")

    for lineno, line in enumerate(file):
        # Ignore blank lines
        if not line.strip():
            continue;

        debug("DEBUG1: " + line)

        # Disregard line/verse boundaries so that repeats can cross lines/verses
        words = line.split()
        debug("DEBUG2: " + "::".join(words))

        # Handle USFM codes (by noting them or dropping them)
        while words:
            word = words.pop(0)
            debug(f"DEBUG3: Processing chunk ::{word}:: with length {len(word)}")
            markerMatch = markerPatternCompiled.search(word)
            #print("DEBUG2: " + "Word=" + word + " " + ' '.join(words))
            # Capture context of book chapter:verse
            if (word == "\\id"):
                debug(f"DEBUG4: Processing id")
                bookid = words.pop(0)
                debug(f"DEBUG5: Found book id {bookid}")
                # We don't process the glossary book
                if (bookid == "XXA" or bookid == "XXB" or bookid == "FRT" or bookid == "GLO" or 
                    bookid == "XXC" or bookid == "XXD" or bookid == "INT" or bookid == "BAK" or
                    bookid == "XXE" or bookid == "XXF" or bookid == "XXG"):
                    file.close()
                    return
                book = bookid # instead of changing to any other naming system, keep it same
                debug("DEBUG6: Set Book = {book}")
            elif (word == "\\c"):
                if not words:
                    error(f"Missing chapter number in {filename}:{lineno}")
                chapter = words.pop(0)
                debug(f"DEBUG7: Chapter {chapter}")
                verse = 0 # restart verse numbering
                mode = NORMAL # move out of PREFIX mode
            elif (word == "\\v"):
                if not words:
                    error(f"Missing verse number in {filename}:{lineno}")
                verse = words.pop(0)
                debug(f"DEBUG8: Verse {verse}")
                # Verse numbers should be monotonically increasing by one every time from the previous one
                prevVerse = int(verseDict.get((book, chapter), 0))
                if ("-" in verse):
                    # Special case: we have a verse range, like 17-18
                    verses = verse.split("-")
                    verse1 = int(verses[0])
                    verse2 = verses[1] # keep it a string for now
                    if (prevVerse+1 != verse1):
                        error(f"Verse number {verse1} in range {verse} is out of sequence in {book} {chapter}, last verse was {prevVerse}")
                    prevVerse = verse1 # move one step forward
                    verse = verse2
                # Now carry on as if no verse range was found
                if (prevVerse+1 != int(verse)):
                    error(f"Verse number {verse} is out of sequence in {book} {chapter}, last verse was {prevVerse}")
                verseDict[(book, chapter)] = verse

    file.close()

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    for filename in files:
        countChaptersVerses(filename)
    print(verseDict)
    save_obj(verseDict, "verses")

if __name__ == '__main__':
    main()
