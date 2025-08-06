#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Change out \SS markers in old-style USFM to \s1, 
# and change \s to \s2 to retain two-level outline"""  """

# Usage: python3 changeSSMarkers.py *.usfm

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: changeSSMarkers.py file [file ...]\n")
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
		#print(f"[{cnt}] " + line, end='')
		# Following code ELIMINATES all \SS lines
		# But I realized that I want to keep them and 
		#if (line.startswith("\\SS")):
		#	print(f"[{file}:{cnt}]\t{line}", end='')
		#else:
		#	fo.write(line)

		line = re.sub(r"\\SS ", r"\\s1 ", line, count=1)
		line = re.sub(r"\\s ", r"\\s2 ", line, count=1)

		fo.write(line)

	fi.close()
	fo.close()

# The end
