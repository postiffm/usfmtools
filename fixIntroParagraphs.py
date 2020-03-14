#!/usr/bin/python3
import os
import re
import sys
import io

# Matt Postiff, 2020
# script to convert \p to \ip in book intros
# Some USFM that we have encountered uses \p in book introductions.
# That is incorrect. The USFM standard specifies \ip for the 
# introductory context.
# All \p before the first \c are changed to \ip

# Each file is backed up first so as not to lose the original data.

# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: fixIntroParagraphs.py file [file ...]\n")
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

	intro_ended = False
	line = 'dummy'

	while line:
		line = fi.readline()
		if line.startswith(r'\c') or line.startswith(r'\v'):
			intro_ended = True
		elif line.startswith(r'\p') and not intro_ended:
			line = line.replace(r'\p', r'\ip')
		fo.writelines([line])
       
	fi.close()
	fo.close()
        
