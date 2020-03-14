#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Change the following characters
# << to U+201C left  double quotation mark
# >> to U+201D right double quotation mark
# < to  U+2018 left  single quotation mark
# > to  U+2019 right single quotation mark

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: chevronsToSmartQuotes.py file [file ...]\n")
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
	fi = io.open(filebak, mode="r", encoding="utf-8")

	# prepare to write modified contents to the original filename
	fo = io.open(file, mode="w", encoding="utf-8")

	for cnt, line in enumerate(fi):
		#print("Working on " + line)
		line = re.sub("<<", "\u201c", line, count=0)
		line = re.sub(">>", "\u201d", line, count=0)
		line = re.sub("<",  "\u2018", line, count=0)
		line = re.sub(">",  "\u2019", line, count=0)
		fo.write(line)

fi.close()
fo.close()
