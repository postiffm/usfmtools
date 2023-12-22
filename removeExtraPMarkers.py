#!/usr/bin/python3
import os
import sys
import io

# Matt Postiff, 2023
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Hunting for \p followed immediately by \s1. Remove the \p marker

# To do:
# Fix error handling. If .bak file already exists, do something smart.

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print("Usage: {script} file [file ...]\n")
    exit(1)

# Count number of \p removed
numPRemoved = 0
lastLinePMarker = False
lastLine = ""

for file in sys.argv:
    print("Processing " + file)
    filebak = file + ".bak"
    if os.path.isdir(file):
        print("Cannot process directory " + file + "\n")
        continue

    # rename the file to .bak
    os.rename(file, filebak)

    # open the new .bak file for input; assume UTF-8 (USFM)
    fi = io.open(filebak, mode="r", encoding="utf-8", newline='')

    # prepare to write modified contents to the original filename
    fo = io.open(file, mode="w", encoding="utf-8", newline='')

    for cnt, line in enumerate(fi):
        line = line.lstrip()
        print("Working on " + line, end="")
        if (line.startswith(r'\s1')):
            print(f"\tFound \s1 marker")

        if (lastLinePMarker == True and line.startswith(r'\s1')):
            fo.write(line) # write this line, but drop the prior \p line
            lastLinePMarker = False
            lastLine = ""
            numPRemoved = numPRemoved + 1
            print(f"\tRemoved \p followed by \s1")
        elif (lastLinePMarker == True and line.startswith(r'\p')):
            # Drop the prior \p line
            numPRemoved = numPRemoved + 1
            print(f"\tRemoved \p followed by \p")
            lastLinePMarker = True # back into \p 'mode' again for next iteration
            lastLine = line
        elif (lastLinePMarker == True):
            # \p followed by other than \p or \s1, so write both
            fo.write(lastLine)
            fo.write(line)
            lastLinePMarker = False
            print(f"\tWrote last two lines")
        elif (line.startswith(r'\p')):
            lastLinePMarker = True
            lastLine = line
            # Hold off doing anything with it until we find out what the next line is
            print(f"\tHolding \p line for further investigation")
        else: # No \p on this line, no \p last line, so just write it
            fo.write(line)
            lastLinePMarker = False
            print(f"\tWriting this line")

    fi.close()
    fo.close()

print (f"    Removed {numPRemoved} \p markers")
