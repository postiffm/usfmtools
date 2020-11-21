#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# Neao Luke is messed up. Need to learn character map to transform from 
# old "floppy disk" type of text to new type of text.

# Usage: python3 nearLearn.py learn.txt

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

needTranslatedDict = {
'\\'  :  '2174',
'i'  :  '4935',
'd'  :  '5068',
' '  :  '28903',
'L'  :  '32',
'U'  :  '2',
'K'  :  '137',
'N'  :  '570',
'e'  :  '5799',
'a'  :  '9129',
'o'  :  '2238',
'u'  :  '2951',
'k'  :  '2363',
'A'  :  '139',
'l'  :  '2853',
'n'  :  '7393',
'F'  :  '46',
's'  :  '1199',
'h'  :  '5087',
'r'  :  '599',
'1'  :  '743',
'9'  :  '163',
'8'  :  '181',
'3'  :  '502',
'\r' :  '5309',
'\n' :  '5309',
'm'  :  '1607',
't'  :  '722',
'<'  :  '169',
'\''  :  '9408',
'B'  :  '72',
'['  :  '4148',
'j'  :  '1523',
'='  :  '6449',
'-'  :  '5962',
','  :  '3538',
'c'  :  '230',
'S'  :  '123',
'I'  :  '58',
'.'  :  '1754',
'+'  :  '150',
'w'  :  '3671',
'>'  :  '2645',
'$'  :  '738',
'4'  :  '362',
'p'  :  '1923',
'T'  :  '52',
'f'  :  '181',
'v'  :  '1267',
'D'  :  '247',
'g'  :  '623',
'b'  :  '1962',
';'  :  '5624',
'y'  :  '2417',
'"'  :  '3186',
'2'  :  '582',
'z'  :  '1529',
'W'  :  '208',
'Z'  :  '682',
'5'  :  '266',
'~'  :  '304',
'E'  :  '58',
':'  :  '254',
'{'  :  '134',
'6'  :  '212',
'J'  :  '259',
'7'  :  '187',
'0'  :  '153',
'V'  :  '10',
'?'  :  '174',
'M'  :  '300',
'G'  :  '50',
'P'  :  '51',
'*'  :  '112',
'O'  :  '12',
'q'  :  '26',
'('  :  '20',
')'  :  '19',
'C'  :  '12',
'H'  :  '2',
}

# The dictionary that we are building...the main goal of this code
# It is augmented in the learnWord function
translateDict = {}
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

def learnWord(old:str, new:str):
    if (old[0] == '\\'):
        # We have a USFM code
        assert(new[0] == '\\'), "New USFM code is not a code: " + new
        # We learn these a whole word at a time, not a character at a time as below
        if (not old in translateDict):
            translateDict[old] = new
            debug(f"\tLearned Marker {old} ==> {new}")
        elif (translateDict[old] != new):
            debug(f"\tERROR!! {old} => {new} but before we learned {old} ==> {translateDict[old]}")
        return

    # Go character by character
    #debug(f"Learning diff between {old} and {new}")
    zipped = zip(old, new)  # results in tuple of same-idx chars
    for o, n in zipped:
        #debug(f"{o}==>{n}")
        # If we wanted to ONLY capture changes, we would enclose below in if (o != n):
        # But I want to capture all character translations, even if x ==> x
        # Something to learn
        if (o in translateDict):
            # We already learned something for this
            if (n != translateDict[o]):
                # Uh oh...we learned something different before
                error(f"{o} => {n} but before we learned {o} ==> {translateDict[o]}")
        else:
            translateDict[o] = n
            debug(f"\tLearned {o} ==> {n}")

def learnLine(oldTxt:str, newTxt:str, oldLine:int, newLine:int):
    debug(f"{oldLine} OLD: {oldTxt}")
    debug(f"{newLine} NEW: {newTxt}")

    old = oldTxt.split()
    new = newTxt.split()
    if (len(old) == len(new)):
        # Process each element
        for i in range(0, len(old)):
            learnWord(old[i], new[i])
    else:
        error("Different number of elements in line; what to do???")
    return


oldTxt = ""
newTxt = ""

for file in sys.argv:
    debug("Processing " + file)
    if os.path.isdir(file):
        error("Cannot process directory " + file + "\n")
        continue

    fi = open(file, mode="r", newline='')

    for cnt, line in enumerate(fi):
        if ((cnt+1) % 3 == 1):
            oldTxt = line
            charmap(oldTxt)
        elif ((cnt+1) % 3 == 2):
            newTxt = line
        elif ((cnt+1) %3 == 0):
            # Should be blank
            assert line == "\r\n", "NOT BLANK: " + str(cnt+1) + ">>" + line + "<<"
            learnLine(oldTxt, newTxt, cnt-1, cnt)

    fi.close()

for o in translateDict:
    print(f"'{o}' : '{translateDict[o]}'")

for c in charDict:
    if (c == "\n"):
        cToPrint = "\\n"
    elif (c == "\r"):
        cToPrint = "\\r"
    elif (c == " "):
        cToPrint = "<spc>"
    else:
        cToPrint = c;
    print(f"{cToPrint}\t{charDict[c]}")

unfound = 0
for n in needTranslatedDict:
    if (n == '\\' or n == '\n' or n == '\r' or n == ' ' or n == 'q'):
        continue
    if not n in translateDict:
        print(f"{n} not found yet")
        unfound += 1
print(f"Not found = {unfound}")

# The end
