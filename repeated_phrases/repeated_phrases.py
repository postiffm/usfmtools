#!/usr/bin/python3

# (c) Jon Snoeberger, 2018
# Make sure you have python3 installed, and
# To run this script on Ubuntu or WSL (Bash on Ubuntu on Windows = Windows Subsystem on Linux), do this:
# sudo apt install python3-pip
# pip3 install 'click'

# Usage: python3 ./repeated_phrases.py pg10.txt out1.txt 5
# Reads in the Project Gutenberg KJV in pg10.txt, puts output to out1, and finds phrases of length >= 5

# Question: how much of the Bible is covered by these phrases?

import click
import re
from operator import itemgetter

def get_repeatseq_KJV(in_file, min_sequencelength, max_sequencelength, bible, repeat_seq):
    """Indexes the whole bible in a massive dictionary. Finds duplicates"""
    file = open(in_file,'r')
    book = ''
    passage = ''
    blank_lines = 0
    lasts = ['']*(max_sequencelength - 1)
    lastadded = 0
    for line in file:
        """This section is customized for the input file"""
        """Check for 4 blank lines, signifying end of book, among other edge cases."""
        if blank_lines == 4:
            if not line.strip():
                continue
            words = line.strip().split()
            if words[-1] == "Solomon":
                book = "Song of Solomon"
            elif words[-1] == "Devine":
                book = "Revelation"
            elif words[-1] == "Apostles":
                book = "Acts"
            elif words[-1] == "Jeremiah" and words[1] == "Lamentations":
                book = "Lamentations"
            else:
                book = words[-1]
                if 'First' in line and 'Moses' not in line:
                    book = "I " + book
                elif 'Second' in line and 'Moses' not in line:
                    book = "II " + book
                elif 'Third' in line and 'Moses' not in line:
                    book = "III " + book
            print(book)
            blank_lines = 0
            lasts = ['']*(max_sequencelength - 1)
            continue

        if not line.strip():
            blank_lines += 1
        else:
            blank_lines = 0
        if book == '':
            continue
        if line == '*** END OF THIS PROJECT GUTENBERG EBOOK THE KING JAMES BIBLE ***\n':
            break
       
        """Split line in words and analyze"""
        words = line.split()
        for word in words:
            if re.match('\\d*:\\d*', word):
                passage = word
                """ The last array contains the last n-1 words to help building the dictionary """
                #for last in lasts:
                #    last = ''
                #lasts = ['']*(max_sequencelength - 1)
                continue
            word = re.sub(r'[^a-zA-Z0-9]+', '', word).lower()
            if word not in bible:
                bible[word] = {},[(book + "_" + passage)] # a "tuple"
            # Go backwards to add short sequences first, then long sequences
            for i in range(lastadded,lastadded - max_sequencelength + 1,-1):
                tree = bible # This doesn't copy the whole data structure; it's just a reference assignment
                if lasts[i] == '':
                    break
                # The "tree" is the whole recursive structure of dictionary of dictionaries that contain dictionaries...
                for j in range(i,lastadded + 1):
                    tree = tree[lasts[j]][0]
                if word in tree: # This means that the phrase is a duplicate
                    if len(tree[word][1]) == 1 and lastadded - i > min_sequencelength:
                        allthewords = []
                        if i<0 and lastadded >= 0:
                            allthewords = lasts[i:] + lasts[0:lastadded + 1]
                        else:
                            allthewords = lasts[i:lastadded + 1]
                        allthewords += [word]
                        if len(allthewords) >= min_sequencelength:
                            repstring = " ".join(allthewords)
                            repeat_seq.append(repstring)
                else:
                    tree[word] = {},[]
                tree[word][1].append((book + "_" + passage))
            lastadded += 1
            if lastadded == max_sequencelength - 1:
                lastadded = 0
            lasts[lastadded] = word

# MAP: Just learning Jon's algorithm by simplifying it to its core pieces...never finished.
def get_repeatseq_simple(in_file, min_sequencelength, max_sequencelength, bible, repeat_seq):
    """Indexes the entire text in a massive dictionary. Finds duplicates"""
    # bible is a dictionary {}
    # repeat_seq is a list []
    file = open(in_file,'r')
    lasts = ['']*(max_sequencelength - 1)
    lastadded = 0 # 
    passage = 0   # identifier for the passage in which the word is found (= line number in this simple case)
    for line in file:
        """Split line in words and analyze"""
        words = line.split()
        for word in words:
            passage += 1 # Fake "passage" info-just line number instead of book:ch:vs
            # Normalize everything to lowercase CHECK THIS LINE
            word = re.sub(r'[^a-zA-Z0-9]+', '', word).lower() # I'm not sure what the re.sub is for
            if word not in bible:
                bible[word] = {},[passage] # a "tuple" of a dictionary and a location for the word

            # Go backwards to add short sequences first, then long sequences
            for i in range(lastadded,lastadded - max_sequencelength + 1,-1):
                tree = bible # This doesn't copy the whole data structure; it's just a reference assignment
                if lasts[i] == '':
                    break
                # The "tree" is the whole recursive structure of dictionary of dictionaries that contain dictionaries...
                for j in range(i,lastadded + 1):
                    tree = tree[lasts[j]][0]
                if word in tree: # This means that the phrase is a duplicate
                    if len(tree[word][1]) == 1 and lastadded - i > min_sequencelength:
                        allthewords = []
                        if i<0 and lastadded >= 0:
                            allthewords = lasts[i:] + lasts[0:lastadded + 1]
                        else:
                            allthewords = lasts[i:lastadded + 1]
                        allthewords += [word]
                        if len(allthewords) >= min_sequencelength:
                            repstring = " ".join(allthewords)
                            repeat_seq.append(repstring)
                else:
                    tree[word] = {},[]
                tree[word][1].append(passage)
            # End for loop

            lastadded += 1
            if lastadded == max_sequencelength - 1:
                lastadded = 0
            lasts[lastadded] = word

def populate_output_array(repeat_seq, bible, output_array):
    for sequence in repeat_seq:
        if sequence == '': # This should never happen...but just in case...
            continue
        keys = sequence.split(' ')
        tree = bible
        for key in keys[:-1]:
            tree = tree[key][0]
        tree = tree[keys[-1]]
        output_array.append([sequence,';'.join(tree[1])])

def clean_repeatseq(output_array):
    """Cleans out duplicate entries. A  6 word duplicate, for instance, contains 2 5 word duplicates"""
    """I don't want to just include the longest string as I find them however. """
    """Meaning, a 5-word string may occur in 3 verses, and a 6-word string in 2 verses, so the final output"""
    """will show both strings (5-word x 3, and 6-word x 2)."""
    """This would remove short strings that are in more places than the duplicated long string"""
    """NOTE: This does not catch the case of a duplicate string longer than max_sequencelength"""
    for i in range(len(output_array)):
        for j in range(i + 1,len(output_array)):
            if output_array[i][0] == '' or output_array[j][0] == '':
                continue
            if output_array[i][1] != output_array[j][1]:
                break
            if output_array[i][0] in output_array[j][0]:
                output_array[i][0] = ''

def concatenate_long_quotes(output_array, max_sequencelength):
    """Takes quotes that should be together and splices them
       for instance "the fox jumped over" and "fox jumped over the" should be "the fox jumped over the
       if and only if they share references. This function only looks at the max_sequencelength sequences."""
    last = -1
    lastwords = []
    lastpassage = ''
    for i in range(len(output_array)):
        phrase, passages = output_array[i]
        words = phrase.split()
        if len(words) != max_sequencelength:
            continue
        if last == -1: # only for the first time around
            last = i
            lastwords = words
            lastpassage = passages
        else:
            match = True
            for j in range(max_sequencelength - 1):
                if words[j] != lastwords[j-max_sequencelength + 1]:
                    match = False
                    break
            if match and passages == lastpassage:
                lastwords.append(words[-1])
                output_array[i][0] = ''
            else:
                output_array[last][0] = ' '.join(lastwords)
                last = i
                lastwords = words
                lastpassage = passages
    output_array[last][0] = ' '.join(lastwords)

@click.command()
@click.argument('in_file', type=click.Path(exists=True))
@click.argument("out_file")
@click.argument("min_sequencelength", type=int)
@click.argument("max_sequencelength", type=int)
def main(in_file, out_file, min_sequencelength, max_sequencelength):
    bible = {}
    repeat_seq = []
    output_array = []
    print("Find repeated phrases")
    #get_repeatseq_KJV(in_file, min_sequencelength, max_sequencelength, bible, repeat_seq)
    get_repeatseq_simple(in_file, min_sequencelength, max_sequencelength, bible, repeat_seq)
    populate_output_array(repeat_seq, bible, output_array)
    bible = {} #free up copius amounts of memory
    print("Removing duplicate duplicates")
    output_array = sorted(output_array,key=itemgetter(1))
    clean_repeatseq(output_array)
    print("Splicing long quotes")
##    concatenate_long_quotes(output_array, max_sequencelength)
    output_array = sorted(output_array)
    print("Writing to file")
    file = open(out_file,'w+')
    for line in output_array:
        if line[0] == '' or not line:
            continue
        file.write(line[0] + '\t' + line[1] + '\n')
    print("Done")

if __name__ == '__main__':
    main()
