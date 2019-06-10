# script to convert \p to \ip in book intros
# Some USFM that we have encountered uses \p in book introductions.
# That is incorrect. The USFM standard specifies \ip for the 
# introductory context.

# run with command: python3 ip.py
# You will want to change the hard-coded paths (lines 8, 24)

import sys  
import os
import re

files = os.listdir('usfm/usfm_rev3')

def convert_ips(in_f, out_f):
	intro_ended = False
	with open(in_f, 'r') as in_fs:
		with open(out_f, 'w') as out_fs:
			line = 'dummy'
			while line:
				line = in_fs.readline()
				if line.startswith(r'\c') or line.startswith(r'\v'):
					intro_ended = True
				elif line.startswith(r'\p') and not intro_ended:
					line = line.replace(r'\p', r'\ip')
				out_fs.writelines([line])

for f in files:
	convert_ips('usfm/usfm_rev3/' + f, 'usfm/usfm_rev3_1/' + f)
  
