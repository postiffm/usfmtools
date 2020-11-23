#!/usr/bin/python3
import os
import re
import sys

# Matt Postiff, 2019
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.
# Change lines like this:
# \rq (Psalm 1:1)
# to look like this:
# \rq (Psalm 1:1) \rq*
# Originally based on my perl replace script. That failed to work because \n in the substitution
# pattern somehow induced perl to put a ^M (carriage return) at the end of every line.
# /c/users/postiffm/Dropbox/AndroidApps/replace 's/\\rq\s([^\r\n]+)/\\rq $1 \\rq*/' 58_Hebrews.usfm
# So I rewrote in Python as a learning experience.
# To do:
# Fix error handling. If .bak file already exists, do something smart.

if len(sys.argv) < 2:
	print("Usage: fixRQMarkers.py file [file ...]")
	exit(1)

script = sys.argv.pop(0)

for file in sys.argv:
	print("Processing " + file)
	filebak = file + ".bak"
	if os.path.isdir(file):
		print("Cannot process directory " + file)
		continue

	# rename the file to .bak
	os.rename(file, filebak)

	# open the new .bak file for input
	fi = open(filebak, 'r')

	# prepare to write modified contents to the original filename
	fo = open(file, 'w')

	# do the regex operation and then write it out
	# This regex is the expression we wish to find
	p = re.compile(r"\\rq ([^\r\n]+)$")
	parens = re.compile(r"\(\s*([^\)]*)\)\s*")
	for cnt, line in enumerate(fi):
		#print("Working on " + line)
		# re::match returns a match object that can be used as below
		m = p.match(line)
		if m != None:
			# Process the match
			rq = m.group(1)  # The contents of the \rq "(Psalm 1:1)" in above example
			# If the actual rq ref has parens around it, delete them
			m = parens.match(rq)
			if (m != None):
				# Update rq to be just the contents of the parens
				rq = m.group(1)
			# Now substitute the original line for the new version with \rq* and no parens
			line = re.sub(
				p,
				r"\\rq " + rq + r" \\rq*",
				line
			)
		fo.write(line)

fi.close()
fo.close()
