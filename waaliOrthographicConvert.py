#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, April 2022
# This script converts the USFM of Waali in accordance with rules
# given to us by Ron Webber. The results are a 
# dictionary that is printed, followed by the conversions.
# This is a test bench.
# See waaliOrthographicConvert2.py for the version that uses the
# same functions but prints out actual USFM.

# Usage: python3 waaliOrthographicConvert.py waaliOrthoTest.SFM > waaliOrthoTest.out

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
    #debug((f"Examining {wrd}, whose last char is {wrd[-1]}"))
    # Remove trailing , or .
    # Notice to match period, you use r".", not "\."
    if ((wrd[-1] == r".") or (wrd[-1] == r',')):
        #debug(f"Removing last char of {wrd}")
        wrd = wrd[:-1]

    # Remove USFM marker at the end of the word like \w or \k*
    # May have to do more than once for like  word\w*\f
    while (True):
        match = regex.search(r"\\[a-z]+(\*)?", wrd)
        if match is not None:
            wrd = wrd.replace(match.group(0), "")
            #debug(f"Removed marker {match.group(0)} from {wrd}")
        else:
            break;

    # Remove other offensive characters
    wrd = wrd.translate({ord(c): None for c in "()«»"})

    if (len(wrd) == 0):
        return

    if (wrd[0] == '\\'):
        # We have a USFM code. Ignore it.
        #debug(f"Ignoring USFM marker: {wrd}")
        return
    elif (regex.search("[0-9]+:[0-9]+", wrd)):
        #debug(f"Ignoring verse range: {wrd}")
        pass
    elif (regex.search("[0-9]+-[0-9]+", wrd)):
        #debug(f"Ignoring numerical range: {wrd}")
        pass
    elif (regex.search("^[0-9]+$", wrd)):
        #debug(f"Ignoring verse number or similar: {wrd}")
        pass
    else:
        if wrd in wordCntDict:
            wordCntDict[wrd] = wordCntDict[wrd]+1
            #debug(f"Seen again: {wrd}")
        else:
            wordCntDict[wrd] = 1
            #debug(f"Added: {wrd}")

def learnLine(line:str):
    #debug(f"LINE: {line}")

    words = line.split()
    for i in range(0, len(words)):
        learnWord(words[i])
    return

# Examples, see waaliOrthoTest.SFM for these and other tests
# 'teng-gbani  > teŋgbane
# (1) ng converted to ŋ  (2) stressed portion ignored  (3) final portion converts vowels
# 'be-fora > befɔra
# bung'vori > boŋ'vori
# 'bi-poga >  bipɔga
# 'Ree-chel > Reekyɛl
# kpe'ji-pegi'yiruu > kpɛgyi pɛgeyiruu (this is actually two words with a hyphen)
def convertConsonants(wrd:str):
    debug(f"Changing consonants in : {wrd}")
    wrd = regex.sub("j", "gy", wrd)
    wrd = regex.sub("J", "Gy", wrd)
    wrd = regex.sub("ch", "ky", wrd)
    wrd = regex.sub("Ch", "Ky", wrd)
    wrd = regex.sub("ng", "ŋ", wrd)  # character U+014B
    wrd = regex.sub("Ng", "Ŋ", wrd)  # character U+014A
    return wrd

def convertUnstressedVowels(wrdPart:str):
    wrdPart = regex.sub("e", "ɛ", wrdPart) # character U+025B
    wrdPart = regex.sub("E", "Ɛ", wrdPart) # character U+0190
    wrdPart = regex.sub("i", "e", wrdPart)
    wrdPart = regex.sub("I", "E", wrdPart)
    wrdPart = regex.sub("o", "ɔ", wrdPart) # character U+0254
    wrdPart = regex.sub("O", "Ɔ", wrdPart) # character U+0186
    wrdPart = regex.sub("u", "o", wrdPart)
    wrdPart = regex.sub("U", "O", wrdPart)
    return wrdPart

def convertVowels(wrd:str):
    # Vowel conversions only happen with close vowels, not "open" ones
    # In other words, we ignored stressed portions of words and convert
    # the vowels in unstressed portions
    debug(f"Changing vowels in : {wrd}")
    # Abstract examples
    # 'XXX-yyy paradigm wor (or 'XXXXXX) where yyy will undergo vowel conversions
    # yyy'XXX paradigm word, where yyy will undergo vowel conversions
    # Strange hyphenated words, like yy'XXX-yyy where yyy will undergo vowel conversions
    # Strange hyphenated words, like yyy'XX-yyy'XXXX where yyy will undergo vowel conversions
    # yyyyyy (no ticks, no apostrophes), which all letters are candidates for vowel conversion
    newWrd = ""
    if (wrd[0] == '\''): # This is a 'XXX-yyy paradigm wor (or 'XXXXXX) where yyy will undergo vowel conversions
        debug(f"Case 1 - 'XXX-yyy paradigm")
        wrdAsList = wrd.split("-", -1) # Split on the hyphen this case
        for wrdPart in wrdAsList:
            if (wrdPart[0] == '\''):
                # This part of the word is stressed, so its vowels remain unchanged (open)
                pass
            else:
                # This part of the word is unstressed, so its vowels need changed (close)
                wrdPart = convertUnstressedVowels(wrdPart)

            newWrd = newWrd + wrdPart # We eliminate the hyphen in the new version of the language
            #NOT FOR NOW newWrd = regex.sub("\'", "", newWrd) # discard apostrophes when work is finalized

    #elif (wrd.find('\'', 1) == 0): # This is a yyy'XXX paradigm word, where yyy will undergo vowel conversions
    #    # The way this was originally written, the comparison was != -1, meaning that at least one ' was found.
    #    # The problem with this was that several ticks could be found, and the assertion below would fail
    #    # I rewrote it as == 1, thinking find returns a count, but it actually returns in INDEX. This 
    #    # was wrong because it would find only words with a tick in the second position (idx = 1).
    #    # I found that I could remove this section entirely and let the next elif cover it all.
    #    # The next elif can cover everything, in fact, but for speed it is good to have a couple of special cases (above and below).
    #    debug(f"Case 2 - yyy'XXX paradigm")
    #    wrdAsList = wrd.split("'", -1) # Split on the apostrophe this case
    #    assert (len(wrdAsList) <= 2), f"ERROR: {wrd} has more than two sections like yyy'XXX'???"
    #    wrdPart = convertUnstressedVowels(wrdAsList[0])
    #    newWrd = wrdPart + '\'' + wrdAsList[1] # must add back in the apostrophe, as the split "deletes" it

    elif (wrd.find('\'', 1) >= 1): # A 'tick' or apostrophe is found some index > 0
        debug(f"Case 3 - state machine")
        # This is most often a word like yyy'XXX where yyy undergoes vowel conversions.
        # This could be a strange word like kpe'ji-pegi'yiruu which is actually two words hyphenated together.
        # This overloads the hyphen, using it like English. Only the close vowels will be changed--those
        # in parts 1 and 3 of the word but not 2 and 4. Build a state machine to handle it.
        CLOSE = 1
        OPEN = 2
        state = CLOSE
        newWrd = ""  # I might be able to make this be the algorithm for the every case.
        for ch in wrd:
            if ch == '\'':
                state = OPEN
                newWrd = newWrd + ch
            elif ch == '-':
                state = CLOSE
                newWrd = newWrd + ch
            else:
                if (state == OPEN): # No vowel conversion
                    newWrd = newWrd + ch 
                else: # State is close, needs vowel conversion
                    newWrd = newWrd + convertUnstressedVowels(ch)

    else: # This is just a regular old word, no initial apostrophe, no mid-apostrophe, so convert all vowels
        debug(f"Case 4: change all vowels")
        newWrd = convertUnstressedVowels(wrd)

    return newWrd

# Main routine
for file in sys.argv:
    #debug("Processing " + file)
    if os.path.isdir(file):
        error("Cannot process directory " + file + "\n")
        continue

    fi = open(file, mode="r", newline='')

    for cnt, line in enumerate(fi):
            learnLine(line)

    fi.close()

for o in wordCntDict:
    convertedWord = convertVowels(convertConsonants(o))
    print(f"{o} : {convertedWord} : {wordCntDict[o]}")

# The end
