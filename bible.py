# Bible information for our work with Bibles International

# Dictionary that gives you a quick conversion from number to canonical book name
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

# Also need function to check that chapters and verses are in proper ranges for every book and chapter of the Bible
def checkChapterInRange(book:str, chapter:int) -> bool:
    return True

def checkVerseInRange(book:str, chapter:int, verse:int) -> bool:
    return True
