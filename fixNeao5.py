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
# line = text to search
# old = the text you are searching for
# new = the text that will replace the old text
# ruleNum is an index into the count array above, to keep track of how many times
#          this particular search/replace is executed
def replaceUSFM(line, old, new, ruleNum):
    global count
    if (regex.search(old, line) != None):
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

        # Round 1: ran 12/8/2021
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

        # Round 2: ran 12/9/2021....about 345 places fixed
        #line = replaceUSFM(line, r"´creedh,", r"´creedhι", 14)  # Verified 15 times
        #line = replaceUSFM(line, r"´CREEDH,", r"´CREEDHƖ", 15)  # Verified 1 times
        #line = replaceUSFM(line, r"Alɛizandr,", r"Alɛizandrι", 16)  # Verified 6 times
        #line = replaceUSFM(line, r"´cʋ,", r"´cʋι", 17) # Verified 6 times
        #line = replaceUSFM(line, r"´Cʋ,", r"´Cʋι", 18) # Verified 2 times
        #line = replaceUSFM(line, r"Moiz,", r"Moizι", 19) # Verified 32 times
        #line = replaceUSFM(line, r"Ezit,", r"Ezitι", 20) # Verified 13 times
        #line = replaceUSFM(line, r"Efɛz,", r"Efɛzι", 21) # Verified 13 times
        #line = replaceUSFM(line, r"wlukιndedh,", r"wlukιndedhι", 22) # Verified 6 times
        #line = replaceUSFM(line, r"˝Nipl,", r"˝Niplι", 23) # Verified 1 time
        #line = replaceUSFM(line, r"˝nipl,", r"˝niplι", 24) # Verified 7 times
        #line = replaceUSFM(line, r"nɛmιɛ,", r"nɛmιɛι", 25) # Verified 2 times
        #line = replaceUSFM(line, r" dh,", r" dhι", 26) # Actually did 227 times; had verified 258 times in Paratext by itself with the capital version
        #line = replaceUSFM(line, r" Dh,", r" Dhι", 27) # Actually did 32 times
    # All of the above done at or before usfm/neao git hash e8bab77

    # Round 3: All below done and committed at usfm/neao git hash 543ae57 12/14/2021
        #line = replaceUSFM(line, r"Zudas,", r"Zudasι", 1) # Verified 18 times
        #line = replaceUSFM(line, r"seaZuifʋn,", r"seaZuifʋnι", 2) # Verified 39 times
        #line = replaceUSFM(line, r"seazuifʋn,", r"seaZuifʋnι", 2) # Verified 1 time; 40 with above
        #line = replaceUSFM(line, r" ‑, ", r" ‑ι ", 3) # Verified 121 times; 122 found by script?
        #line = replaceUSFM(line, r"Glɛk,", r"Glɛkι", 4) # Verified 18 times, e.g. Acts 6:1
        #line = replaceUSFM(line, r"Glek,", r"Glɛkι", 4) # Verified 1 time, total 19 with above, Acts 17:12
        #line = replaceUSFM(line, r" s, ", r" sι ", 5) # Verified 23 times
        #line = replaceUSFM(line, r"Ananias,", r"Ananiasι", 6) # Verified 10 times
        #line = replaceUSFM(line, r" An,", r" Anι", 7) # Verified 3 times
        #line = replaceUSFM(line, r" ´z, ", r" ´zι ", 8) # Verified 9 times
        #line = replaceUSFM(line, r"´Jrʋgɔɔbhʋ,", r"´Jrʋgɔɔbhʋι", 9) # Verified 1 time
        #line = replaceUSFM(line, r" gl, ", r" glι ", 10) # Verified 10 times
        #line = replaceUSFM(line, r" nyn,", r" nynι", 11)  # Verified 10 times, like Acts 5:37, but without tone mark
        #line = replaceUSFM(line, r"Elɔd,", r"Elɔdι", 12)  # Verified 20 times
        #line = replaceUSFM(line, r"Pɔns,", r"Pɔnsι", 13)  # Verified 1 time
        #line = replaceUSFM(line, r"klandh,", r"klandhι", 14)  # Verified 2 times
        #line = replaceUSFM(line, r"bhʋ,", r"bhʋι", 15)  # Verified 43 times; 42 found by this script?
        #line = replaceUSFM(line, r"Izaak,", r"Izaakι", 16)  # Verified 3 times
        #line = replaceUSFM(line, r"˝Duud,", r"˝Duudι", 17)  # Verified 2 times
        #line = replaceUSFM(line, r"˝duud,", r"˝duudι", 18)  # Verified 2 times
        #line = replaceUSFM(line, r"Paatɛs,", r"Paatɛsι", 19)  # Verified 1 time ???
        #line = replaceUSFM(line, r"Silɛn,", r"Silɛnι", 20)  # Verified 5 times
        #line = replaceUSFM(line, r"gbl,", r"gblι", 21)  # Verified 5 times
        #line = replaceUSFM(line, r" D,", r" Dι", 22)  # Verified 6 times, all at start of sentence. 7 found by script is correct; Paratext missed one
        #line = replaceUSFM(line, r"Klɛt,", r"Klɛtι", 23)  # Verified 3 times

    # Round 4: All below done and committed at usfm/neao git hash 6ffbbb0 12/15/2021
        #line = replaceUSFM(line, r"´W,", r"´Wι", 1)  # 9 times, always beginning of sentence
        #line = replaceUSFM(line, r"waann.aw,", r"waannawι", 2)  # 2 times Acts 10:12, 11:6 extra period 
        #line = replaceUSFM(line, r"Waannaw,", r"Waannawι", 3)  # 1 time Mark 4:4
        #line = replaceUSFM(line, r"waannaw,", r"waannawι", 4)  # 1 time Mark 4:32
        #line = replaceUSFM(line, r"Taas,", r"Taasι", 5)  # 3 times
        #line = replaceUSFM(line, r"w,", r"wι", 6)  # 5 times
        #ine = replaceUSFM(line, r"Silis,", r"Silisι", 7)  # 1 time
        #line = replaceUSFM(line, r"Damas,", r"Damasι", 8)  # 8 times
        #line = replaceUSFM(line, r"‑d,", r"‑dι", 9)  # 11 times
        #line = replaceUSFM(line, r"pood,", r"poodι", 10)  # 2 times
        #line = replaceUSFM(line, r"Pood,", r"Poodι", 11)  # 1 times
        #line = replaceUSFM(line, r"Antiɔs,", r"Antiɔsι", 12)  # 14 times
        #line = replaceUSFM(line, r"Etiɛn,", r"Etiɛnι", 13)  # 9 times
        #line = replaceUSFM(line, r"Paamιnas,", r"Paamιnasι", 14)  # 1 time
        #line = replaceUSFM(line, r"´klejedh,", r"´kle´jedhι", 15)  # 3 times

    # Round 5: All below done and committed at usfm/neao git hash 0d56351 (12/16/2021)
        #line = replaceUSFM(line, r"bhʋdh,", r"bhʋdhι", 1)  # 3 times
        #line = replaceUSFM(line, r"´y,", r"´yι", 2)  # 26 times
        #line = replaceUSFM(line, r"paadh,", r"paadhι", 3)  # 14 times
        #line = replaceUSFM(line, r"legliz,", r"leglizι", 4)  # 30 times
        #line = replaceUSFM(line, r"Azɔt,", r"Azɔtι", 5)  # 1 times
        #line = replaceUSFM(line, r"´klejeɛ‑", r"´kle´jeɛ‑", 6)  # 24 times
        #ine = replaceUSFM(line, r"´Klejeɛ‑", r"´Kle´jeɛ‑", 7)  # 2 times
        #line = replaceUSFM(line, r"Lid,", r"Lidι", 8)  # 3 times
        #line = replaceUSFM(line, r"Dɔɔkas,", r"Dɔɔkasι", 9)  # 2 times
        #line = replaceUSFM(line, r"´wl,", r"´wlι", 10)  # 1 times Acts 9:39
        #line = replaceUSFM(line, r"˝wwli", r"wwli˝", 11)  # 506 times
        #line = replaceUSFM(line, r"Legliz,", r"Leglizι", 12)  # 4 times, see above rule 4, capitalized version of it
    
    # Round 6: All below done and committed at usfm/nheao git hash ___ (12/18/2021)
        line = replaceUSFM(line, r"kr,", r"krι", )  # 4 times  Mark 16:10, Acts 11:30, 21:35; 1Pe 4:11 (with a tone mark error too fixed by hand)
        line = replaceUSFM(line, r"Mak,", r"Makι", )  # 6 times Mark 1:0 2x, Acts 12:12, 12:25, 15:37, 1pe 5:13
        line = replaceUSFM(line, r"nιn,", r"nιnι", )  # 3 times Mark 7:4, 8, Acts 12:10
        line = replaceUSFM(line, r"Lod,", r"Lodι", )  # 5 times Acts 12:13, 18:2, 23:26, Rev 4:3, 21:19 which covers Lod, Klod, and emelod,
        line = replaceUSFM(line, r"lod,", r"lodι", )  # Combined with above
        line = replaceUSFM(line, r"Felis,", r"Felisι", )  # 10 times
        line = replaceUSFM(line, r"´yι,", r"´yιι", )  # 3 times
        line = replaceUSFM(line, r"wwɛɛan", r"wwɛɛ.an", )  # 51 times. This is very strange to have a period mid-word.
        line = replaceUSFM(line, r"Liitr,", r"Liitrι", )  #  7 times
        line = replaceUSFM(line, r"nyʋsʋ,", r"nyʋsʋι", )  # 4 times
        line = replaceUSFM(line, r"Nyʋsʋ,, r"Nyʋsʋι", )  # 1 time, combined with above
        line = replaceUSFM(line, r"Masedoan,", r"Masedoanι", )  # 10 times

        fo.write(line)

fi.close()
fo.close()

for i in range(1, len(count)):
    print(f"Fixed rule {i} {count[i]} times")
