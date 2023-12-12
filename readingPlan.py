# To assist creating simple Bible reading plans for SAB >= 11.1
# Matt Postiff (c) 2023 postiffm@gmail.com

usfmIDToChapters = {
    "GEN" : 50,
    "EXO" : 40,
    "LEV" : 27,
    "NUM" : 36,
    "DEU" : 34,
    "JOS" : 24,
    "JDG" : 21,
    "RUT" : 4, 
    "1SA" : 31,
    "2SA" : 24,
    "1KI" : 22,
    "2KI" : 25,
    "1CH" : 29,
    "2CH" : 36,
    "EZR" : 10,
    "NEH" : 13,
    "EST" : 10,
    "JOB" : 42,
    "PSA" : 150,
    "PRO" : 31,
    "ECC" : 12,
    "SNG" : 8, 
    "ISA" : 66,
    "JER" : 52,
    "LAM" : 5, 
    "EZK" : 48,
    "DAN" : 12,
    "HOS" : 14,
    "JOL" : 3, 
    "AMO" : 9, 
    "OBA" : 1, 
    "JON" : 4, 
    "MIC" : 7, 
    "NAM" : 3, 
    "HAB" : 3, 
    "ZEP" : 3, 
    "HAG" : 2, 
    "ZEC" : 14,
    "MAL" : 4, 
    "MAT" : 28,
    "MRK" : 16,
    "LUK" : 24,
    "JHN" : 21,
    "ACT" : 28,
    "ROM" : 16,
    "1CO" : 16,
    "2CO" : 13,
    "GAL" : 6, 
    "EPH" : 6, 
    "PHP" : 4, 
    "COL" : 4, 
    "1TH" : 5, 
    "2TH" : 3, 
    "1TI" : 6, 
    "2TI" : 4, 
    "TIT" : 3, 
    "PHM" : 1, 
    "HEB" : 13,
    "JAS" : 5, 
    "1PE" : 5, 
    "2PE" : 3, 
    "1JN" : 5, 
    "2JN" : 1, 
    "3JN" : 1, 
    "JUD" : 1, 
    "REV" : 22,
}

# Convert above to a list of tuples, slice that list
OTBooks = list(usfmIDToChapters.items())[0:39] # not including 39
NTBooks = list(usfmIDToChapters.items())[39:67]
#print(OTBooks)
#print(NTBooks)

def NTOnce():
    print("\\id NTOnce")
    print("\\title Read through the New Testament in 9 months")
    print("\\descr Read Matthew through Revelation one chapter at a time.")
    # print("\\img plan1.img")

    day = 1
    for book, chapters in NTBooks:
        for ch in range(1, chapters+1):
            print(f"\\day {day}")
            print(f"\\ref {book} {ch}")
            day = day + 1

def OTOnce():
    print("\\id OTOnce")
    print("\\title Read through the Old Testament in two and a half years")
    print("\\descr Read Genesis through Malachi one chapter at a time.")
    # print("\\img plan1.img")

    day = 1
    for book, chapters in OTBooks:
        for ch in range(1, chapters+1):
            print(f"\\day {day}")
            print(f"\\ref {book} {ch}")
            day = day + 1

#NTOnce()
OTOnce()