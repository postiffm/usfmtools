#!/usr/bin/python3
# This is just a learning script.

import sys
import pickle

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

# Usage: ../../usfmtools/readDict.py verses
# The file read is verses.pkl (.pkl is automatically added)
# This reads the dictionary file and prints it. Should match
# what you saved.
def main():
    file = sys.argv[1]
    print(f"Reading from {file}")
    verseDict = load_obj(file)
    print("Data type after reload : ", type(verseDict)) 
    print(verseDict)

if __name__ == '__main__':
    main()