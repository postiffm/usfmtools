#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2022
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Change the following characters

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: poundTo00BA.py file [file ...]\n")
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
	fi = io.open(filebak, mode="r", encoding="utf-8", newline='')

	# prepare to write modified contents to the original filename
	fo = io.open(file, mode="w", encoding="utf-8", newline='')

	# To deal with the escapes, see stackoverflow.com/questions/58328587/ppython-3-7-4-re-error-bad-escape-s-at-position-0
	# Warning about \z as an invalid escape sequence
	newStr = "\\\zhash \u00ba \\\zhash*"
	print(f"newStr = {newStr}")

	for cnt, line in enumerate(fi):
		#print("Working on " + line)
		# Because the escapes are confusing, I am using a pre-made string here 
		# instead of a string literal
		line = re.sub("#", newStr, line, count=0)
		fo.write(line)

fi.close()
fo.close()
