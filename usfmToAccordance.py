#!/usr/bin/python3

# (c) Matt Postiff, 2020
# This script converts USFM into an Accordance-compliant (very simplified) text file
#
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'

# Usage:
# python3 usfmToAccordance.py test1.usfm > test1.txt

import copy
import click
import re
from operator import itemgetter
import functools

# Find all phrases of length=sequencelength, repeated more than once, from in_file
def convertUSFMToAccordance(filename):
    """Scans the entire USFM and re-formats for Accordance"""
    # Modes that the usfm scanner is in
    NORMAL = 0
    MARKER = 1
    PREFIX = 2
    mode = PREFIX
    usfmCode = ""
    # The current word list
    wordlist = []
    file = open(filename,'r')
    print(f"Processing file {filename}")
    for line in file:
        # Ignore blank lines
        if not line.strip():
            continue;

        print("DEBUG: " + line, end='')

        # Disregard line/verse boundaries so that repeats can cross lines/verses
        words = line.split()

        # Handle USFM codes (by dropping them out)
        while words:
            word = words.pop(0)
            print("DEBUG: " + ' '.join(words))
            if (word == "\\id"):
                book = words.pop(0)
                print(f"Found book {book}")
            elif (word == "\\c"):
                chapter = words.pop(0)
                print(f"Found chapter {chapter}")
            elif (word == "\\v"):
                verse = words.pop(0)
                print(f"Found verse {verse}")
                output.append(book)
                output.append(chapter)
                output.append(verse)
                mode = NORMAL
            else:
                print("Fell into else clause")
                matchstr = "\\\\S+\\s"
                print(matchstr)
                p = re.compile(matchstr) # looking for a usfm \marker
                m = p.match(word)
                if (m != None):
                    usfmCode = m.group(1)
                    mode = MARKER
                    print(f"Found marker \{usfmCode}")
            
    # Close the file
    file.close()

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    for filename in files:
        convertUSFMToAccordance(filename)

if __name__ == '__main__':
    main()
