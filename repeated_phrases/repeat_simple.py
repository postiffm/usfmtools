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

import copy
import click
import re
from operator import itemgetter
import functools

# Class that contains the necessary tracking information about a repeated-phrase
class RepeatedPhrase:
    def __init__(self, count):
        self.count = count
        self.locations = []
        self.endVerses = []
        self.length = 0

    def increment(self):
        self.count = self.count + 1

    def addLocation(self, loc):
        self.locations.append(loc)

    def addEndVerse(self, verse):
        # It is a bit of a challenge to know where the repeated phrase
        # begins because we don't know until we are at the end of it that it is 
        # a match! So I record the verse where the phrase ends. Kind of a pain.
        self.endVerses.append(verse)

    def setLength(self, len):
        self.length = len

# For reducing a list like this: [-1, -1, -1, 25]
# to a single number: 1.
# Or, a list like this: [8, 23] to the single number 2.
# The idea is to add one for every non-negative-1 in
# the list.
def my_add(lis):
    result = 0
    for x in lis:
        if (x != -1): result = result + 1
    return result

# Find all phrases of length=sequencelength, repeated more than once,from in_file
def find_repeated_phrases(in_file, sequencelength:int):
    """Scans the entire text using a "window" and finds duplicates and stores in dictionary"""
    wordlist = []
    file = open(in_file,'r')
    seqDict = {}
    seqDictCleaned = {}
    wordCnt = 0;

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
            wordCnt = wordCnt + 1
            wordlist.append(word)
            if (len(wordlist) > sequencelength):
                wordlist.pop(0)

            # Initial condition: if we are not yet up to the required length, go to the next word
            if (len(wordlist) < sequencelength):
                continue;

            # Have we see this sequence of words before?
            # First convert the wordlist to a string to use it to index a dictionary
            idxStr = ' '.join(wordlist)
            rephrase = seqDict.get(idxStr, RepeatedPhrase(0));
            rephrase.increment()
            rephrase.addLocation(wordCnt)
            rephrase.addEndVerse(book+" "+chapter+":"+verse)
            rephrase.setLength(sequencelength)
            #print("inc=" + str(rephrase.count) + " loc=" + str(rephrase.locations))
            #if (count >= 1):
            #    print("We have a repeated phrase: " + ' '.join(wordlist))
            seqDict[idxStr]=rephrase  # don't have to do copy.deepcopy here...RepeatedPhrase() above creates the new object
            
    # Close the file
    file.close()

    # Print a summary of the information and create a clean copy with only repeated phrases in it.
    # This will be much smaller than the working copy.
    
    #print("Size of repeated phrase dictionary is " + str(len(seqDict)))
    for key in seqDict:
        rephrase = seqDict[key]
        if (rephrase.count > 1):
            #print(str(rephrase.count) + "--" + key + "--" + ' '.join(rephrase.endVerses) + "--" + str(rephrase.length) + "--" + str(rephrase.locations))
            seqDictCleaned[key] = rephrase;

    #print("Size of repeated phrase dictionary is " + str(len(seqDictCleaned)))
    return [seqDictCleaned, wordCnt]

@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.argument("min_sequencelength", type=int)
@click.argument("max_sequencelength", type=int)
def main(in_file, min_sequencelength, max_sequencelength):
    # Print HTML output header
    print('''
<html>
<head>
<style>
  p.greek { background-color:lightgray; text-indent: 25px; }
  p.bold { font-weight: bold; }
</style>
</head>
<body>
''')

    # Load repeated phrases of all the lengths requested
    rpDicts = [dict() for x in range (0, max_sequencelength+1)]
    print("<p>Finding repeated phrases of " + str(min_sequencelength) + " words to " + str(max_sequencelength) + " words long...</p>")
    for i in range(max_sequencelength, min_sequencelength-1, -1):
        rpDicts[i], wordCnt = find_repeated_phrases(in_file, i)
        #print("Size of repeated phrase dictionary is " + str(len(rpDicts[i])))
    
    print('<p>Found ' + str(wordCnt) + ' words in the text')
    
    # Clean out smaller phrases that are found in larger phrases
    # Algorithm is to start with the smallest phrases and work up 
    # toward the larger ones. So if a 2-word phrase--the exact
    # 2-word phrase--is found in a 3-word phrase, then we can 
    # remove it from consideration. We have to keep track of
    # word indexes in order for this to work, which adds some
    # complexity to the data structure and adds tracking code.
    finalRPDict = {}
    for i in range(min_sequencelength, max_sequencelength, 1):
        # If sequencelengths are 5 and 7, this will loop 
        # for 5 and 6, but not 7
        # I am comparing rpDicts[i] and rpDicts[i+1]
        rpDict1 = rpDicts[i]
        rpDict2 = rpDicts[i+1]

        # Note that i and i+1 are the respective lengths of the repeated phrases

        for key1 in rpDict1:
            found = False;
            # Can I find this key in rpDict2?
            # key1 could be in any of rpDict2's phrases
            rp1 = rpDict1[key1]
            for key2 in rpDict2:
                rp2 = rpDict2[key2]
                # Now the complexity is that we have to see if key1 in any of its locations
                # is found in any of key2's locations. If so, then those "duplicate" locations
                # must be removed from our consideration. But the "un-duplicate" locations
                # must be retained.
                if (key1 in key2):
                    # This /could/ be a sub-phrase...depends on exact location in the Bible.
                    # It has to be wholly within rp2, then it is a repeat and we can ignore it
                    # since it is already covered in the longer phrase. But some instances of 
                    # it could be contained in a longer phrase while other instances are
                    # not...and we cannot delete the "not" ones.
                    for i in range(0, len(rp1.locations)): # loc1 in rp1.locations:
                        loc1 = rp1.locations[i]
                        for loc2 in rp2.locations:
                            if ( (loc1 <= loc2) and ((loc1 - i + 1) >= (loc2- (i+1) + 1)) ):
                                # This is a sub-phrase of an already-known longer phrase, so we mark 
                                # it as not interesting.
                                rp1.locations[i] = -1; # -1 flags the location as duplicated
                                break
            for loc1 in rp1.locations:
                if (loc1 != -1):
                    # This is a unique phrase not repeated in a longer one
                    finalRPDict[key1] = rp1
                    break;

    # Since the longest phrases are "for sure" not duplicated by anything longer...at least
    # that we looked for in this run of the code...we just append them to the dictionary.
    finalRPDict.update(rpDicts[max_sequencelength])

    # Print out all repeated phrases
    print('<p class="bold">All ' + str(len(finalRPDict)) + ' repeated phrases...</p>')
    wordsCovered = 0
    wordsTranslated = 0
    for key in finalRPDict:
        rephrase = finalRPDict[key]
        print('<p>' + str(rephrase.count)  + " repeats of a " + str(rephrase.length) + " word-phrase in " + ' '.join(rephrase.endVerses) + " w/ location map=" + str(rephrase.locations) + '</p>')
        print('<p class="greek">' + key + '</p>')
        # Figure out how many words this covers and add to total
        # Step 1: Count the number of "not -1 phrases" in the repphrase.locations[] list
        count = my_add(rephrase.locations)
        # Step 2: Multiply that count by the length of the phrase
        # print("\tAdding " + str(rephrase.length*count))
        wordsCovered = wordsCovered + rephrase.length * count
        wordsTranslated = wordsTranslated + rephrase.length

    print('<p>Total words covered by repeated phrases is {0:d} ({1:.1f} % of text)</p>'.format(wordsCovered, wordsCovered/wordCnt*100))
    print('<p>Total words translated would be {0:d} ({1:.1f}% of text)</p>'.format(wordsTranslated, wordsTranslated/wordCnt*100))

    # Print HTML footer
    print('</body>')

if __name__ == '__main__':
    main()
