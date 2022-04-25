#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, April 23, 2022
# This script converts the USFM of Waali in accordance with rules
# given to us by Ron Webber. The results are a new USFM file. Old
# one is renamed .bak

def replaceUSFM(line, old, new, ruleNum):
    global count
    if (regex.search(old, line) != None):
        count[ruleNum] = count[ruleNum] + len(regex.findall(old, line))
        line = regex.sub(old, new, line)

    return line

DEBUG = 0
def debug(msg:str, lineEnd=''):
    if (DEBUG):
        print(msg) # end=lineEnd)

def error(msg:str):
    print(f"ERROR: {msg}")

script = sys.argv.pop(0)

if len(sys.argv) < 1:
	print("Usage: {script} file [file ...]\n")
	exit(1)

# Examples, see waaliOrthoTest.SFM for these and other tests
# 'teng-gbani  > teŋgbane
# (1) ng converted to ŋ  (2) stressed portion ignored  (3) final portion converts vowels
# 'be-fora > befɔra
# bung'vori > boŋ'vori
# 'bi-poga >  bipɔga
# 'Ree-chel > Reekyɛl
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
    newWrd = ""
    if (wrd[0] == '\''): # This is a 'XXX-yyy paradigm wor (or 'XXXXXX) where yyy will undergo vowel conversions
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

    elif (wrd.find('\'', 1) == 1): # was != -1 # This is a yyy'XXX paradigm word, where yyy will undergo vowel conversions
        wrdAsList = wrd.split("'", -1) # Split on the apostrophe this case
        assert (len(wrdAsList) <= 2), f"ERROR: {wrd} has more than two sections like yyy'XXX'???"
        wrdPart = convertUnstressedVowels(wrdAsList[0])
        newWrd = wrdPart + '\'' + wrdAsList[1] # must add back in the apostrophe, as the split "deletes" it

    elif (wrd.find('\'', 1) > 1): # More than one 'tick' or apostrophe.
        # This is a strange word like kpe'ji-pegi'yiruu which is actually two words hyphenated together.
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
                if (state == OPEN):
                    newWrd = newWrd + ch # No conversion
                else:
                    newWrd = newWrd + convertUnstressedVowels(ch)

    else: # This is just a regular old word, no initial apostrophe, no mid-apostrophe, so convert all vowels
        newWrd = convertUnstressedVowels(wrd)

    return newWrd

for file in sys.argv:
    print("Processing " + file)
    filebak = file + ".bak"
    if os.path.isdir(file):
        print("Cannot process directory " + file + "\n")
        continue

    # rename the file to .bak
    os.rename(file, filebak)

    # open the new .bak file for input; assume UTF-8 (USFM)
    fi = io.open(filebak, mode="r", encoding="utf-8", newline='')

    # prepare to write modified contents to the original filename
    fo = io.open(file, mode="w", encoding="utf-8", newline='')

    for cnt, line in enumerate(fi):
        #print(f"Processing line {cnt}")
        if (line.find('\\id') != -1):
            fo.write(line) # do not change the \id line, just write it out as is
            continue
        words = line.split(' ', -1) # Split on spaces
        newLine = ""
        for word in words:
            #print(f"Proessing {word}")
            if (len(word) == 0): # Two spaces gives us a "empty" string
                pass
            elif (word[0] == '\\'): # Ignore USFM markers
                pass
            else: # Convert this word; will touch some non Waali text, but OK for now
                word = convertVowels(convertConsonants(word))

            newLine = newLine + word + ' '

        newLine = newLine.strip() + "\n" # Remove extra space at end that I added
        fo.write(newLine)

    fi.close()
    fo.close()

# End for loop
