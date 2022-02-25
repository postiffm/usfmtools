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
# python3 usfmToAccordance.py ../Luxembourgish\ NT/usfm_rev2/*.SFM > LuxAcc.txt 

# Test cases are found in test[1-n].usfm

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

def convertUSFMToAccordance(filename, paragraphMarkers):
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
                    bookid == "XXE" or bookid == "XXF" or bookid == "XXG" or bookid == "CNC" or
                    bookid == "TDX" or bookid == "OTH"):
                    file.close()
                    return
                book = canonicalBookName[bookid]
            elif (word == "\\c"):
                if not words:
                    error(f"Missing chapter number in {filename}:{lineno}")
                chapter = words.pop(0)
                mode = NORMAL # move out of PREFIX mode
            elif (word == "\\v"):
                if not words:
                    error(f"Missing verse number in {filename}:{lineno}")
                verse = words.pop(0)
                if (justStarted == False):
                    print(f"\n{book} {chapter}:{verse}", end='')
                else:
                    # No newline at the start, but instead a byte-order-mark for UTF-8
                    #print('\xEF\xBB\xBF', end='') # produces c3af c2bb c2bf ??
                    #sys.stdout.buffer.write(b"\xEF\xBB\xBF") # avoids encoding step
                    # In future, I recommend to myself to specify output file and 
                    # open it in mode write with encoding utf-8 and see what happens
                    # All the work to figure out above is nought: Accordance doesn't
                    # like the BOM.
                    print(f"{book} {chapter}:{verse}", end='')
                    justStarted = False
                if ((newParagraph == True) and (paragraphMarkers == True)):
                    print(" ¶", end='')
                    newParagraph = False # reset
                mode = NORMAL
            # Capture whether we are starting a new paragraph...for future use
            elif (word == "\\p"):
                newParagraph = True
            elif (mode != PREFIX and markerMatch != None): # word is a USFM marker
                usfmCode = markerMatch.group(1)
                if ('*' in usfmCode): # end marker
                    debug(f"Found endmarker \{usfmCode} in {word}")
                    mode = NORMAL
                elif (usfmCode == "w"):
                    # Special case: \w Kéiert ëm|ëmkéieren\w*,
                    # or: \w Léiermeeschtere vum Gesetz|Léiermeeschter vum Gesetz\w*
                    # A glossary-marked word with a lexical form. The lexical form
                    # needs to be removed.
                    mode = GLOSSARY
                elif (usfmCode in markersToIgnore): # formatting markers like \li, q1
                    #print(f"Found to-ignore marker \{usfmCode} in {word}")
                    mode = NORMAL
                else:
                    #print(f"Found regular marker \{usfmCode} in {word}")
                    mode = MARKER
            elif (mode == GLOSSARY):
                # Within \w ... \w*, we have to watch for the | symbol because
                # it specifies the lexical form of a word.
                #print("In GLOSSARY mode...")
                if (word.find('|') != -1): # | found
                    # We must strip the |... off, print the first part,
                    # and then drop into mode=MARKER so that the 
                    # rest of the words up to \w* are dropped. The code
                    # below splits the word on |, and this returns a list,
                    # of which I want the first element, before the |.
                    strippedWord = word.split('|', 1)[0]
                    printWord(strippedWord)
                    mode = MARKER
                else:
                    printWord(word)
            elif (mode == NORMAL):
                # The fall-through case is simply to print the word
                printWord(word)
            
    file.close()

def printWord(word):
    # If the "word" is just a punctuation marker, we don't 
    # want to put a space before it! But some words have
    # punctuation already, so we cannot simply look at the last
    # character. I look at word[0] because I have found strings like this:
    # last word inside quote,'  where the word=,' and I need to smash
    # that whole thing right next to the previous word.
    if (word[0] == '.' or word[0] == ',' or word[0] == ';' or word[0] == ':' or word[0] == '!' or word[0] == '?'):
        print(word, end='');
    else:
        print(" " + word, end='')

@click.command()
@click.option('--para/--no-para', default=True, help='Default true. If set, turns on paragraph markers in output.')
@click.argument('files', nargs=-1)
def main(para, files):
    """Given USFM input files, creates a single Accordance-compatible import text file."""
    for filename in files:
        convertUSFMToAccordance(filename, para)

if __name__ == '__main__':
    main()
