#!/usr/bin/python3

# (c) Matt Postiff, 2020
# This script lists all USFM markers found in the text.
#
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'
# pip3 install regex

# Usage:
# python3 findMarkers.py test1.usfm

import copy
import click
#import re
import regex
from operator import itemgetter
import functools
import os.path

# Our USFM markers that are approved for use by translators
# Note that mt, s, and q are not officially on the approved list, 
# but since they are synonymous with their \mtq, \s1, and \q1 identities,
# no problem to keep them here.
ApprovedMarkers = {
  # Identification
  'id', 'rem', 'h', 'toc1', 'toc2', 'toc3', 'mt', 'mt1', 'mt2', 
  # Introductions
  'ili', 'imt1', 'imt2', 'is', 'ip', 'ipr', 'imq', 'iot', 'io1', 'io2', 'io3', 'ior', 'ior*', 'ie', 
  # Headings, references
  'ms', 's', 's1', 's2', 'r', 'd', 'qa', 'rq', 'rq*', 'x', 'x*', 'xo',
  # Chapters and verses
  'c', 'v', 
  # Paragraphs
  'p', 'm', 'mi', 'nb', 'b',
  # Poetry
  'q', 'q1', 'q2', 'qc', 'qs', 'qs*',
  # Lists
  'li1', 'li2',
  # Footnotes
  'f', 'f*', 'fr', 'fk', 'ft',
  # Special Text
  'nd', 'nd*', 'qt', 'qt*', 'tl', 'tl*', 'w', 'w*', 'xt', 'xt*',
  # Add-ons (confused if \k..\k* is allowed or not)
  'k', 'k*', 'tr', 'th1', 'th2', 'th3', 'th4', 'th5', 'tc1', 'tc2', 'tc3', 'tc4', 'tc5',
  'periph'
}

def findUSFMMarkers(filename, markerDB:{}):
    """Scans the entire USFM and finds markers"""
    usfmCode = ""
    markerPattern = r'\\([a-zA-Z0-9]+\*{0,1})'
    markerPatternCompiled = regex.compile(markerPattern) # looking for a usfm \marker

    wordlist = []
    file = open(filename,'r')
    #print(f"Processing file {filename}")
    for line in file:
        # Ignore blank lines
        if not line.strip():
            continue;

        words = line.split()

        while words:
            word = words.pop(0)
            # To find a single USFM marker, use the following (usual case):
            #markerMatch = markerPatternCompiled.search(word)
            #if (markerMatch != None): # word is a USFM marker

            # But lines sometimes have multiple markers, so have to loop through:
            for markerMatch in regex.finditer(markerPatternCompiled, word):
                usfmCode = markerMatch.group(1)
                #print(f"Marker {usfmCode}")
                count = markerDB.get(usfmCode, 0)
                markerDB[usfmCode] = count + 1;
            
    # Close the file
    file.close()

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        print("Usage: python3 findMarkers.py *.usfm")
        exit(1)

    markerDB = {}
    for filename in files:
        if (os.path.exists(filename)):
            findUSFMMarkers(filename, markerDB)

    for marker in markerDB:
        print(f"{marker}\t{markerDB[marker]}", end='')
        if (not (marker in ApprovedMarkers)):
            print("\t<<== This marker is not in the BI approved list")
        else:
            print("")

if __name__ == '__main__':
    main()
