#!/usr/bin/python3

# (c) Matt Postiff, 2020
# This script finds text prints occurrences of it highlighted.
#
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'
# pip3 install regex

# Usage:
# python3 highlightText.py "nang" test2.usfm
# Test cases: test2.usfm test7.usfm (n, and ,n examples)
# In AndroidApps/usfm/neao, say:
# python3 highlightText.py "n," *.SFM
# and it should print all lines that have the phrase "n," in them.

# View output with Firefox or other web browser

import copy
import click
import regex
from operator import itemgetter
import functools
import sys

DEBUG = 1
def debug(msg:str, lineEnd=''):
    if (DEBUG):
        print(msg) # end=lineEnd)

def error(msg:str):
    #print(f"ERROR: {msg}")
    sys.exit(f"ERROR: {msg}")

def findText(searchstring:str, filename:str):
    """Scans the entire USFM finds relevant strings"""

    file = open(filename,'r')
    debug(f"Processing file {filename}")
    for line in file:
        line = line.rstrip()
        # Corresponds to grep $'\u2011\,'
        #pattern = r'\u2011\,'
        pattern = searchstring
        #debug(f"Pattern = {pattern}")
        patternCompiled = regex.compile(pattern)
        patternMatch = patternCompiled.search(line)
        if (patternMatch != None):
            # Replace all occurrences (count=0) of pattern in line with <span...>
            #line = regex.sub(pattern, "JUNK", line, count=0)
            line = patternCompiled.sub('<span style="color:red">'+pattern+'</span>', line, count=0)
            print(f"<p>{line}</p>");

    file.close()

@click.command()
@click.argument('searchstring')
@click.argument('files', nargs=-1)
def main(searchstring:str, files):
    for filename in files:
        findText(searchstring, filename)

if __name__ == '__main__':
    main()
