#!/usr/bin/python3

# (c) Matt Postiff, 2020
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'

# Usage: python3 ./repeat_simple.py pg10.txt out1.txt 3
# Reads in the Project Gutenberg KJV in pg10.txt, puts output to out1, and finds phrases of length >= 5

# Question: how much of the Bible is covered by these phrases?

import click
import re
from operator import itemgetter

def get_repeatseq_simple(in_file, sequencelength):
    """Indexes the entire text in a massive dictionary. Finds duplicates"""
    # bible is a dictionary {}
    # repeat_seq is a list []
    wordlist = []
    file = open(in_file,'r')
    seqDict = {}
    for line in file:
        # Ignore line (verse) boundaries
        words = line.split()
        for word in words:
            # Normalize every word; 'r' = raw; first part
            # removes any punctuation, etc. and then we lowercase it.
            word = re.sub(r'[^a-zA-Z0-9]+', '', word).lower()

            # wordlist is a moving window on the list of words, always trying to keep it
            # sequencelength words long.
            wordlist.append(word)
            if (len(wordlist) > sequencelength):
                wordlist.pop(0)

            # Initial condition: if we are not yet up to the required length, go to the next word
            if (len(wordlist) < sequencelength):
                continue;

            # Have we see this sequence of words before?
            # First convert the wordlist to a string to use it to index a dictionary
            idxStr = ''.join(wordlist)
            count = seqDict.get(idxStr, 0);
            if (count >= 1):
                print("We have a repeated phrase: " + ' '.join(wordlist))
            seqDict[idxStr]=count+1

            # To do: add smarts to do various lengths; print at end so don't get repeats; don't avoid repeats; 

@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.argument("out_file")
@click.argument("min_sequencelength", type=int)
@click.argument("max_sequencelength", type=int)
def main(in_file, out_file, min_sequencelength, max_sequencelength):
    print("Find repeated phrases")
    get_repeatseq_simple(in_file, max_sequencelength)

if __name__ == '__main__':
    main()
