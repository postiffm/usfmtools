#!/usr/bin/python3
import os
import regex
import sys
import io

# Matt Postiff, December 7, 2021
# Do a python regex operation on a bunch of files, editing those files in place.
# Each file is backed up first so as not to lose the original data.

# Explanation: Replace all commas-after-ton-markings with ι iota

count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def replaceUSFM(line, old, new, ruleNum):
    global count
    if (regex.search(old, line) != None): # Verified ok; 42 times
        count[ruleNum] = count[ruleNum] + len(regex.findall(old, line))
        line = regex.sub(old, new, line)

    return line

script = sys.argv.pop(0)

if len(sys.argv) < 1:
	print("Usage: {script} file [file ...]\n")
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
    fi = io.open(filebak, mode="r", encoding="utf-8", newline='')

    # prepare to write modified contents to the original filename
    fo = io.open(file, mode="w", encoding="utf-8", newline='')

    for cnt, line in enumerate(fi):
        # I have verified that there are no occurrences remaining of 
        # comma-' and comma-'' tone markings. There is also the - tone marker.
        # -, seems find throughout. ,- also seems fine.

        # Ran the below on 12/8/2021
        #line = replaceUSFM(line, r"nʋʋdh,", r"nʋʋdhι", 1)  # Verified ok; 42 times
        #line = replaceUSFM(line, r" ´, ",   r" ´ι ", 2)    # Verified ok; 16 times
        #line = replaceUSFM(line, r" ‑: ",   r" ‑Ɔ ", 3)    # Verified ok; 29 times
        #line = replaceUSFM(line, r"Baanabas,", r"Baanabasι", 4)  # Verified 32 times
        #line = replaceUSFM(line, r"Pilat,", r"Pilatι", 5)  # Verified 38 times
        #line = replaceUSFM(line, r"´nyn,", r"´nynι", 6)  # Verified 250 times
        #line = replaceUSFM(line, r"Nazalɛt,", r"Nazalɛtι", 7)  # Verified 19 times
        #line = replaceUSFM(line, r"Zak,", r"Zakι", 7)  # Verified 14 times
        #line = replaceUSFM(line, r"Zud,", r"Zudι", 8)  # Verified 2 times
        #line = replaceUSFM(line, r"ZUD,", r"ZUDƖ", 9)  # Verified 2 times
        #line = replaceUSFM(line, r"´kp,", r"´kpι", 10)  # Verified 68 times
        #line = replaceUSFM(line, r"Kandas,", r"Kandasι", 11)  # Verified 2 times
        #line = replaceUSFM(line, r"gm,", r"gmι", 12)  # Verified 46 times
        #line = replaceUSFM(line, r"Gm,", r"Gmι", 13)  # Verified 5 times

        # Ran the following on 12/9/2021....about 345 places fixed
        line = replaceUSFM(line, r"´creedh,", r"´creedhι", 14)  # Verified 15 times
        line = replaceUSFM(line, r"´CREEDH,", r"´CREEDHƖ", 15)  # Verified 1 times
        line = replaceUSFM(line, r"Alɛizandr,", r"Alɛizandrι", 16)  # Verified 6 times
        line = replaceUSFM(line, r"´cʋ,", r"´cʋι", 17) # Verified 6 times
        line = replaceUSFM(line, r"´Cʋ,", r"´Cʋι", 18) # Verified 2 times
        line = replaceUSFM(line, r"Moiz,", r"Moizι", 19) # Verified 32 times
        line = replaceUSFM(line, r"Ezit,", r"Ezitι", 20) # Verified 13 times
        line = replaceUSFM(line, r"Efɛz,", r"Efɛzι", 21) # Verified 13 times
        line = replaceUSFM(line, r"wlukιndedh,", r"wlukιndedhι", 22) # Verified 6 times
        line = replaceUSFM(line, r"˝Nipl,", r"˝Niplι", 23) # Verified 1 time
        line = replaceUSFM(line, r"˝nipl,", r"˝niplι", 24) # Verified 7 times
        line = replaceUSFM(line, r"nɛmιɛ,", r"nɛmιɛι", 25) # Verified 2 times
        line = replaceUSFM(line, r" dh,", r"dhι", 26) # Actually did 227 times; had verified 258 times in Paratext by itself with the capital version
        line = replaceUSFM(line, r" Dh,", r"Dhι", 27) # Actually did 32 times

        #if (regex.search(r"˝,", line) != None):  # Pattern too broad
        #    count[1] = count[1] + len(regex.findall(r"˝,", line))
        #    line = regex.sub(r"˝,", r"˝ι", line)

        # Can't be sure yet on this one because Nathan did not mark some
        # " s," which are stand-alone s, words. Most s, are spsd to be sι instead
        #if (regex.search(r"s,", line) != None):
        #    count[4] = count[4] + len(regex.findall(r"s,", line))
        #   line = regex.sub(r"s,", r"sι", line)

        fo.write(line)

fi.close()
fo.close()

for i in range(1, len(count)):
    print(f"Fixed rule {i} {count[i]} times")
