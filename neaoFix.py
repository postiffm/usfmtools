#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# Neao Luke is messed up. Take character map is largely produced 
# by neaoLearn.py learn.txt, but I had to do some hand modifications
# to fix some bugs. Use that to rebuild Luke from the floppy disk files.

# Usage: python3 neaoFix.py learn.txt

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

translateDict = {
'\\id' : '\\id',
'L' : 'L',
'U' : 'U',
'K' : 'K',
'N' : 'N',
'e' : 'e',
'a' : 'a',
'o' : 'o',
'u' : 'u',
'k' : 'k',
'A' : 'A',
'l' : 'l',
'n' : 'n',
'F' : 'F',
'i' : 'i',
's' : 's',
'h' : 'h',
'r' : 'r',
'1' : '1',
'9' : '9',
'8' : '8',
'3' : '3',
'\\mt' : '\\mt',
'<' : 'ι',
'\'' : '´',
'B' : 'B',
'[' : 'ʋ',
'd' : 'd',
'j' : 'j',
'=' : 'ɛ',
'-' : '-',
'\\h' : '\\h',
',' : 'ι',
'\\c' : '\\c',
'\\q' : '\\q',
'\\SS' : '\\s1',
'\\rm' : '\\rq',  # \rm is an old-school marker, I guess
'I' : 'I',
'.' : '.',
'+' : 'Ɛ',
'w' : 'w',
'>' : ',',
'$' : ':',
'4' : '4',
'\\s' : '\\s2',
'p' : 'p',
'T' : 'T',
'f' : 'f',
'\\p' : '\\p',
'\\v' : '\\v',
'D' : 'D',
'g' : 'g',
'b' : 'b',
';' : 'ɔ',
':' : 'Ɔ',
'y' : 'y',
'"' : '˝',
'c' : 'c',
't' : 't',
'2' : '2',
'z' : 'z',
'm' : 'm',
'W' : 'W',
'Z' : 'Z',
'5' : '5',
'~' : '~',
'6' : '6',
'7' : '7',
'0' : '0',
'v' : 'v',
'(' : '(',
'M' : 'M',
')' : ')',
'{' : 'Ʋ',
'?' : '?',
'E' : 'E',
'J' : 'J',
'S' : 'S',
'V' : 'V',
'G' : 'G',
'P' : 'P',
'\\po' : '\\q1', # poetic line, a GUESS
'\\pm' : '\\q2', # poetic line, a GUESS
'\\eq' : '\\m', # GUESS that it was "end quote" but not sure
'\\b' : '\\b', # \b blank line USFM marker GUESS
'\\m' : '\\m', # \m margin paragraph USFM marker GUESS
'\\r' : '\\r', # \r USFM marker
'\r' : '\r',   # carriage return 0xd
'\n' : '\n',   # line feed 0xa
' '  : ' ',
'*' : ';',
'O' : 'O',
'C' : 'C',
'H' : 'H',
}

DEBUG = 1
def debug(msg:str, lineEnd=''):
    if (DEBUG):
        print(msg) # end=lineEnd)

def error(msg:str):
    print(f"ERROR: {msg}")

for file in sys.argv:
    debug("Processing " + file)
    if os.path.isdir(file):
        error("Cannot process directory " + file + "\n")
        continue

    fi = open(file, mode="r", newline='')

    for cnt, line in enumerate(fi):
        for c in line:
            if (c == '\r'):
                pass
            elif (c == '\\'): # USFM Marker upcoming; start it; this turns on "marker mode" in this parser
                marker = '\\'
            elif (marker != ''): # Building up or finishing the USFM marker
                if (c == ' ' or c == '\n' or c == '\r'): # Done w/ marker; start it on a new line
                    print(f"\n{translateDict[marker]} ", end='')
                    marker = '';
                else:  # Add another character to the marker
                    marker = marker+c
            else: # a non-USFM-marker
                if (c == '\n' or c == '\r'):
                    # Do not print newline; wait until a marker shows up, and then print a newline
                    # But we do have to print a space to start cramming the next line onto this
                    # same line
                    print(' ', end='')
                elif (translateDict.get(c)):
                    print(f"{translateDict[c]}", end='')
                else:
                    # Cannot find the character in the translate dictionary
                    error("Cannot find character '" + c + "' in translate dictionary")
    
    print("") # add a newline at the end just in case
    fi.close()

# The end
