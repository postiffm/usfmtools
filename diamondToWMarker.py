#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2021
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Explanation: The diamond marker is used by BI to indicate
# a gossary word. It is actually a Unicode Lozenge (U+25CA)
# which is encoded in UTF-8 as hex e2 97 8a. We are doing this:
# Abraham◊.   ==>  \w Abraham\w*.

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: diamondToWMarker.py file [file ...]\n")
	exit(1)

# This takes care of cases where "words" begin with punctuation.
# Like “Hosana◊! 
def addInitialSlashW(word):
	if (word[0] == '“' or word[0] == '‘'):
		# Splice in a \w-space after that character
		word = word[0] + "\w " + word[1:]
	else:
		word = "\w " + word
	return word

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

	for cnt, line in enumerate(fi):
		#print("Working on " + line)
		words = line.split()
		while words:
			word = words.pop(0)
			if (word[-1] == "\u25ca"):
				print(f"Found {word} ends with diamond marker. ", end='')
				word = re.sub("\u25ca", "\\\\w*", word)
				word = addInitialSlashW(word)
				print(f"Replaced with {word}")
			elif ('\u25ca' in word):
				print(f"Found {word} has embedded diamond marker. ", end='')
				word = re.sub("\u25ca", "\\\\w*", word)
				word = addInitialSlashW(word)
				print(f"Replaced with {word}")
			else:
				# No diamond marker at all
				pass
			fo.write(word + " ")
		fo.write('\r\n')

fi.close()
fo.close()
