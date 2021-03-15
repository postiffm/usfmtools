# Bible information for our work with Bibles International

# Dictionary that gives you a quick conversion from number to canonical book name,
# that is, the user-visible nice form of the name that BI uses for book abbreviations.
numberToBook = {
1: "Gen", 
2: "Exo", 
3: "Lev", 
4: "Num", 
5: "Deu", 
6: "Jos", 
7: "Jdg", 
8: "Rut", 
9: "1Sa", 
10: "2Sa",
11: "1Ki",
12: "2Ki",
13: "1Ch",
14: "2Ch",
15: "Ezr",
16: "Neh",
17: "Est",
18: "Job",
19: "Psa",
20: "Pro",
21: "Ecc",
22: "Sol",
23: "Isa",
24: "Jer",
25: "Lam",
26: "Eze",
27: "Dan",
28: "Hos",
29: "Joe",
30: "Amo",
31: "Oba",
32: "Jon",
33: "Mic",
34: "Nah",
35: "Hab",
36: "Zep",
37: "Hag",
38: "Zec",
39: "Mal",
# 40 is missing on purpose, although some USFM does have Matthew as book 40
41: "Mat",
42: "Mar",
43: "Luk",
44: "Joh",
45: "Act",
46: "Rom",
47: "1Co",
48: "2Co",
49: "Gal",
50: "Eph",
51: "Phi",
52: "Col",
53: "1Th",
54: "2Th",
55: "1Ti",
56: "2Ti",
57: "Tit",
58: "Phm",
59: "Heb",
60: "Jam",
61: "1Pe",
62: "2Pe",
63: "1Jo",
64: "2Jo",
65: "3Jo",
66: "Jud",
67: "Rev" 
}

# Reverse of the above dictionary. This lets you get from name to book number
bookToNumber = dict((book, number) for number, book in numberToBook.items())
# Notice how this dictionary is set up as a bunch of pairs book->number, by
# looking up the (number->book) entries in the above dictionary. This works
# because there is a one-to-one mapping in the original dictionary.

# Fix up book names, like Gen., so they are what we expect - no trailing periods, etc.
# I expect there will be lots of other lookups we need to do here, like another table 
# to translate from one style of name to another. We shall see what the data presents to us.
def normalizeBook(book:str) -> str:
    if (book[-1] == "."):
        book = book[0:-1]
    if (bookToNumber.get(book) == None):
        print(f"Error: Book name {book} not found in canonical book list")
        exit(1)
    return book

#==========================================================================
# Here is an explanation of the 11 digit scripture reference encoding
#
#	First Zero (digit #1) = placeholder
#	Next two digits (digits #2, 3) = Bible book code
#		GEN = "01"
#		MAL = "39"
#		MAT = "41" (skip #40)
#		REV = "67"
#	Next 3 digits (digits #4, 5, 6) = chapter
#		ch. 1 = "001"
#		ch. 34 = "034"
#		ch. 119 = "119" (the highest #)
#	Next 3 digits(digits #7, 8, 9) = verse
#		[same idea as the chapter]
#	Last 2 Zeros (digits #10, 11) = placeholders
#	
# Examples:
#	Gen. 1:1 =	   "00100100100"
#	Psa. 119:172 = "01911917200"
#	Rev. 22:21 =   "06702202100"
#
# The refEncode function expects book
#==========================================================================
def refEncode(book:str, ch:int, vs:int) -> str:
    book = normalizeBook(book)
    return "0" + f"{bookToNumber[book]:02d}" + f"{ch:03d}" + f"{vs:03d}" + "00"

# Testing code
def testRefEncode():
    print(refEncode("Gen", 1, 1))
    print(refEncode("Psa", 119, 172))
    print(refEncode("Rev", 22, 21))
    print(refEncode("Gen.", 1, 1))
    print(refEncode("Psa.", 119, 172))
    print(refEncode("Rev.", 22, 21))
    #print(refEncode("GEn", 22, 21)) # this book is not found
    #print(refEncode("Abc", 22, 21)) # neither is this book found

#testRefEncode()

# Dictionary for quick conversion of non-standard but nice-to-print book abbreviations
# with periods
usfmIDToShortBookName = {
"GEN" : "Gen.",
"EXO" : "Ex.",
"LEV" : "Lev.",
"NUM" : "Num.",
"DEU" : "Deut.",
"JOS" : "Josh.",
"JDG" : "Judg.",
"RUT" : "Ruth",
"1SA" : "1Sam.",
"2SA" : "2Sam.",
"1KI" : "1Kings",
"2KI" : "2Kings",
"1CH" : "1Chr.",
"2CH" : "2Chr.",
"EZR" : "Ezra",
"NEH" : "Neh.",
"EST" : "Esth.",
"JOB" : "Job",
"PSA" : "Psa.",
"PRO" : "Prov.",
"ECC" : "Eccl.",
"SNG" : "Song",
"ISA" : "Is.",
"JER" : "Jer.",
"LAM" : "Lam.",
"EZK" : "Ezek.",
"DAN" : "Dan.",
"HOS" : "Hos.",
"JOL" : "Joel",
"AMO" : "Amos",
"OBA" : "Obad.",
"JON" : "Jonah",
"MIC" : "Mic.",
"NAM" : "Nah.",
"HAB" : "Hab.",
"ZEP" : "Zeph.",
"HAG" : "Hag.",
"ZEC" : "Zech.",
"MAL" : "Mal.",
"MAT" : "Matt.",
"MRK" : "Mark",
"LUK" : "Luke",
"JHN" : "John",
"ACT" : "Acts",
"ROM" : "Rom.",
"1CO" : "1Cor.",
"2CO" : "2Cor.",
"GAL" : "Gal.",
"EPH" : "Eph.",
"PHP" : "Phil.",
"COL" : "Col.",
"1TH" : "1Th.",
"2TH" : "2Th.",
"1TI" : "1Tim.",
"2TI" : "2Tim.",
"TIT" : "Titus",
"PHM" : "Philem.",
"HEB" : "Heb.",
"JAS" : "James",
"1PE" : "1Pet.",
"2PE" : "2Pet.",
"1JN" : "1John",
"2JN" : "2John",
"3JN" : "3John",
"JUD" : "Jude",
"REV" : "Rev.",
}

# This maps to the above canonical book name, that is, the user-visible
# nice form of the name that BI uses for book abbreviations.
usfmIDToBook = {
"GEN" : "Gen", 
"EXO" : "Exo", 
"LEV" : "Lev", 
"NUM" : "Num", 
"DEU" : "Deu", 
"JOS" : "Jos", 
"JDG" : "Jdg", 
"RUT" : "Rut", 
"1SA" : "1Sa", 
"2SA" : "2Sa",
"1KI" : "1Ki",
"2KI" : "2Ki",
"1CH" : "1Ch",
"2CH" : "2Ch",
"EZR" : "Ezr",
"NEH" : "Neh",
"EST" : "Est",
"JOB" : "Job",
"PSA" : "Psa",
"PRO" : "Pro",
"ECC" : "Ecc",
"SNG" : "Sol",
"ISA" : "Isa",
"JER" : "Jer",
"LAM" : "Lam",
"EZK" : "Eze",
"DAN" : "Dan",
"HOS" : "Hos",
"JOL" : "Joe",
"AMO" : "Amo",
"OBA" : "Oba",
"JON" : "Jon",
"MIC" : "Mic",
"NAM" : "Nah",
"HAB" : "Hab",
"ZEP" : "Zep",
"HAG" : "Hag",
"ZEC" : "Zec",
"MAL" : "Mal",
"MAT" : "Mat",
"MRK" : "Mar",
"LUK" : "Luk",
"JHN" : "Joh",
"ACT" : "Act",
"ROM" : "Rom",
"1CO" : "1Co",
"2CO" : "2Co",
"GAL" : "Gal",
"EPH" : "Eph",
"PHP" : "Phi",
"COL" : "Col",
"1TH" : "1Th",
"2TH" : "2Th",
"1TI" : "1Ti",
"2TI" : "2Ti",
"TIT" : "Tit",
"PHM" : "Phm",
"HEB" : "Heb",
"JAS" : "Jam",
"1PE" : "1Pe",
"2PE" : "2Pe",
"1JN" : "1Jo",
"2JN" : "2Jo",
"3JN" : "3Jo",
"JUD" : "Jud",
"REV" : "Rev" 
}

numberOfChapters = {
    "Gen": 50,
    "Exo": 40,
    "Lev": 27,
    "Num": 36,
    "Deu": 34,
    "Jos": 24,
    "Jdg": 21,
    "Rut": 4,
    "1Sa": 31,
    "2Sa": 24,
    "1Ki": 22,
    "2Ki": 25,
    "1Ch": 29,
    "2Ch": 36,
    "Ezr": 10,
    "Neh": 13,
    "Est": 10,
    "Job": 42,
    "Psa": 150,
    "Pro": 31,
    "Ecc": 12,
    "Sol": 8,
    "Isa": 66,
    "Jer": 52,
    "Lam": 5,
    "Eze": 48,
    "Dan": 12,
    "Hos": 14,
    "Joe": 3,
    "Amo": 9,
    "Oba": 1,
    "Jon": 4,
    "Mic": 7,
    "Nah": 3,
    "Hab": 3,
    "Zep": 3,
    "Hag": 2,
    "Zec": 14,
    "Mal": 4,
    "Mat": 28,
    "Mar": 16,
    "Luk": 24,
    "Joh": 21,
    "Act": 28,
    "Rom": 16,
    "1Co": 16,
    "2Co": 13,
    "Gal": 6,
    "Eph": 6,
    "Phi": 4,
    "Col": 4,
    "1Th": 5,
    "2Th": 3,
    "1Ti": 6,
    "2Ti": 4,
    "Tit": 3,
    "Phm": 1,
    "Heb": 13,
    "Jam": 5,
    "1Pe": 5,
    "2Pe": 3,
    "1Jo": 5,
    "2Jo": 1,
    "3Jo": 1,
    "Jud": 1,
    "Rev": 22
}

# Also need function to check that chapters and verses are in proper ranges for every book and chapter of the Bible
def checkChapterInRange(book:str, chapter:int) -> bool:
    book = normalizeBook(book)
    if (chapter > 0 and chapter <= numberOfChapters.get(book)):
        return True
    print(f"Error: Chapter {chapter} is out of range for {book}")
    return False

def testChapterRange():
    checkChapterInRange("Gen.", 56)
    checkChapterInRange("Rev", 21)
    checkChapterInRange("Mat", 0)

#testChapterRange()

# For saving and restoring the above verse dictionary to a file
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)

load_obj()

def checkVerseInRange(book:str, chapter:int, verse:int) -> bool:
    book = normalizeBook(book)
    return True

def testVerseRange():
    checkVerseInRange("Gen.", 50, 240)
    checkVerseInRange("Rev", 21, 0)
    checkVerseInRange("Mat", 1, 20)
    checkVerseInRange("Mat", 1, 29)
    return True

testVerseRange()
