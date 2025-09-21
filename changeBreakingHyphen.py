#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Change out '-' normal breaking hyphen to \u2011, non-breaking hyphen
#
# Usage: python3 changeBreakingHyphen.py *.usfm

# To do:
# Fix error handling. If .bak file already exists, do something smart.

script = sys.argv.pop(0)

if len(sys.argv) < 1:
    print(f"Usage: {script} file [file ...]\n")
    exit(1)

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
	fi = open(filebak, mode="r", newline='')

	# prepare to write modified contents to the original filename
	fo = open(file, mode="w", newline='')

	for cnt, line in enumerate(fi):
		# Replace '-' with \u2011 (UTF-8 encoding)
		# The regular hyphen is \u002d, the standard "ASCII" hyphen
		line = line.replace('-', '\u2011')
		fo.write(line)

	fi.close()
	fo.close()

# The end
