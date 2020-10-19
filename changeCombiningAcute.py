#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Change out 0xCC 0x81 "combining acute accent" in old-style USFM to 
# 0xC2 0xB4 which is a regular stand-alone acute accent. That is, change the 
# UTF-32 0x00000301 to UTF-32 0x000000B4
#
# Do the same for the combining double accent U+030B (UTF-8 CC8B) and 
# change it out to U+02DD (UTF-8 CB9D)

# Usage: python3 changeCombiningAcute.py *.usfm

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: changeCombiningAcute.py file [file ...]\n")
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

	for cnt, line in enumerate(fi):
		# Replace cc81 with c2b4 (UTF-8 encoding)
		# Which is same as changing U0301 to U00B4
		line = line.replace('\u0301', '\u00B4')
		# Same with U+030B to U+02DD
		line = line.replace('\u030B', '\u02DD')
		fo.write(line)

	fi.close()
	fo.close()

# The end
