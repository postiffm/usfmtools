#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, 2020
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Find (\xt ...) and change to (\xt ... \xt*) if
# the ending marker is not already there

script = 'fixMissingXTMarkers.py'

# Usage: python3 <script> file.usfm

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

script = sys.argv.pop(0)

for file in sys.argv:
    print("Processing " + file)
    filebak = file + ".bak"
    if os.path.isdir(file):
        print("Cannot process directory " + file + "\n")
        continue

    # rename the file to .bak
    os.rename(file, filebak)

    # open the new .bak file for input; assume UTF-8 (USFM)
    # Note: cannot do io.open(..., mode="rb", encoding="utf-8") as not permitted in this version of Python
    # The newline argument in both open statements is critical to leave alone the CRLF
    # lines. I don't want to edit files and change every line ending and have that 
    # end up as a diff in git. It obscures what is really going on.
    fi = open(filebak, mode="r", newline='')

    # prepare to write modified contents to the original filename
    fo = open(file, mode="w", newline='')

    xtpattern = regex.compile(r"\(\\xt ([^*]+)\)")

    for cnt, line in enumerate(fi):
        #print(f"[{cnt}] " + line, end='')
        # This can be done in two ways. (1) without a compiled regex
        #line = regex.sub(r"\(\\xt ([^*]+)\)", r"(\\xt \1\\xt*)", line)
        # or (2) with a compiled regex
        line = xtpattern.sub(r"(\\xt \1\\xt*)", line)

        fo.write(line)

    fi.close()
    fo.close()

# The end
