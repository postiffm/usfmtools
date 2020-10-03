#!/usr/bin/python3

# (c) Matt Postiff, 2020
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'

# Usage:
# python3 ./repeat_simple.py data1.txt out1.txt 3 8
# python3 ./repeat_simple.py ../../bibles/byzusfm/40_Matthew.usfm out2.txt 5 5

# # Reads in the Project Gutenberg KJV in pg10.txt, puts output to out1, and finds phrases of length >= 5

# Question: how much of the Bible is covered by these phrases?

import click
import re
from operator import itemgetter

# Find all phrases of length=sequencelength, repeated more than once,from in_file
def find_repeated_phrases(in_file, sequencelength:int):
    """Indexes the entire text in a massive dictionary. Finds duplicates"""
    wordlist = []
    file = open(in_file,'r')
    seqDict = {}
    seqDictCleaned = {}
    locDict = {}
    wordCnt = 0
    for line in file:
        # Ignore blank lines
        if not line.strip():
            continue;
        
        # Disregard line/verse boundaries so that repeats can cross lines/verses
        
        words = line.split()
        
        # Following is designed to handle byzusfm simple USFM files
        if (words[0] == "\\id"):
            book = words[1]
        elif (words[0] == "\\c"):
            chapter = words[1]

        if (words[0] != "\\v"):
            continue; # this is not verse text in USFM
        else:
            words.pop(0) # remove \v
            verse = words.pop(0) # remove verse number
        wordCnt += len(words)

        #print(' '.join(words))

        for word in words:
            # Normalize every word; 'r' = raw; first part
            # removes any punctuation, etc. and then we lowercase it.
            #word = re.sub(r'[^a-zA-Z0-9]+', '', word).lower() no work on Greek
            word = re.sub(r'[,\.]+', '', word)
            #print(word)

            # wordlist is a moving window on the list of words, always keeping it
            # sequencelength words long. We look at each new window and compare it to
            # the other windows we have seen, stored in a fancy dictionary.
            wordlist.append(word)
            if (len(wordlist) > sequencelength):
                wordlist.pop(0)

            # Initial condition: if we are not yet up to the required length, go to the next word
            if (len(wordlist) < sequencelength):
                continue;

            # Have we see this sequence of words before?
            # First convert the wordlist to a string to use it to index a dictionary
            idxStr = ' '.join(wordlist)
            count = seqDict.get(idxStr, 0);
            #if (count >= 1):
            #    print("We have a repeated phrase: " + ' '.join(wordlist))
            seqDict[idxStr]=count+1
            locDict[idxStr]=locDict.get(idxStr,"")+" "+book+" "+chapter+":"+verse
            # To do: add smarts to do various lengths; print at end so don't get repeats; don't avoid repeats; 

    # Print a summary of the information and create a clean copy with only repeated phrases in it.
    # This will be much smaller than the working copy.
    print("Found " + str(wordCnt) + " words in the text")
    print("Size of repeated phrase dictionary is " + str(len(seqDict)))
    for key in seqDict:
        count = seqDict[key]
        if (count > 1):
            print(str(count) + " " + key + " " + locDict[key])
            seqDictCleaned[key] = count;

    #print("Size of repeated phrase dictionary is " + str(len(seqDictCleaned)))
    return seqDictCleaned

@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.argument("out_file")
@click.argument("min_sequencelength", type=int)
@click.argument("max_sequencelength", type=int)
def main(in_file, out_file, min_sequencelength, max_sequencelength):
    # Load repeated phrases of all the lengths requested
    rpDicts = [dict() for x in range (0, max_sequencelength+1)]
    for i in range(max_sequencelength, min_sequencelength-1, -1):
        print("\nFind repeated phrases of " +str(i) + " words...")
        rpDicts[i] = find_repeated_phrases(in_file, i)
        print("Size of repeated phrase dictionary is " + str(len(rpDicts[i])))
    
    # Clean out smaller phrases that are found in larger phrases
    

    # Print out all repeated phrases

if __name__ == '__main__':
    main()
