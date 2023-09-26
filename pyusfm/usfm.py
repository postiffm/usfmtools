# USFM tools
# (c) Matt Postiff, 2022-2023
# Experimental coding project for USFM processing

import regex
import json

# Class that handles generic USFM "stuff"
class Usfm:
    # Simple: \p, \b
    # Moderate: \id MAT, \c 1, \v 1
    # Complex: \v 18 \x + \xo 2:18 \xt Gen 35:19; Jér 31:15\x*A ma yanga na Rama, 
    # I believe we will keep this generic to handle marker, argument, and generic content
    # and then specialize this class with child classes for specific markers.
    def __init__(self, Marker, Arg="", Content=""):
        self.marker = Marker
        self.arg = Arg
        self.content = Content

    def print(self):
        # But I have to re-constitute the content
        if (self.arg == ""):
            print(f'{self.marker} {self.content}')    
        else:
            print(f'{self.marker} {self.arg} {self.content}')

# Specialized classes for specific USFM markers
class UsfmC(Usfm):
    # \c #
    def __init__(self, Marker, Number, ):
        super().__init__(Marker, Number, "")
        self.number = Number
    def print(self):
        print(f'{self.marker} {self.number}')

class UsfmP(Usfm):
    # \p (paragraph marker)
    def __init__(self, Marker="p", Content=""):
        super().__init__(Marker, "", Content)
    def print(self):
        print(f'{self.marker} {self.content}')

class UsfmV(Usfm):
    # \v # verse text
    def __init__(self, Marker, Number, Text):
        super().__init__(Marker, Number, Text)
        self.number = Number
        self.text = Text
    def print(self):
        print(f'{self.marker} {self.number} {self.text}')

class UsfmS(Usfm):
    # \s# Heading
    def __init__(self, Marker, Heading):
        super().__init__(Marker, "", Heading)
        self.heading = Heading
    def print(self):
        print(f'{self.marker} {self.heading}')

class UsfmId(Usfm):
    # \id MAT <other text may appear here>
    def __init__(self, Marker, Id, OtherText):
        super().__init__(Marker, Id, OtherText)
        self.id = Id
    def print(self):
        print(f'{self.marker} {self.id}')

class Book:
    # The layout of USFM is fairly flat, with a chapter mainly consisting
    # of a list of USFM elements one after the other. Some are nested, but
    # many are not.
    
    # My idea is to have a usfm elem have its marker and content text/elements
    # and (if any) endmarker as well. Keeping it general will help to make
    # tree traversal easier.
    def __init__(self, BookName):
        self.name = BookName
        self.id = ""
        # Book contains a list of USFM elements (next) which may themselves
        # contain other USFM elements
        self.usfms = []
    
    def printInternals(self):
        print(f'Data for {self.name}')
        for u in self.usfms:
            print(type(u))

    def load(self, FileName):
        """Reads in the entire USFM and stores it in our nascent data model"""
        usfmCode = ""
        markerPattern = r'\\([a-zA-Z0-9]+\*{0,1})'
        markerPatternCompiled = regex.compile(markerPattern) # looking for a usfm \marker

        file = open(FileName,'r')
        for line in file:
            # Ignore blank lines
            if not line.strip():
                continue;

            words = line.split()
            # Get the first marker
            u = ""
            marker = words.pop(0)
            #print(f'MARKER = {marker}')
            if (marker == r"\v"):  # Note that without rawstring, \v is a special character
                u = UsfmV(marker, words.pop(0), str(' '.join(words)))
            elif (marker == "\c"):
                u = UsfmC(marker, words.pop(0))
            elif (marker == "\p"):
                u = UsfmP(marker, str(' '.join(words)))
            elif (marker == "\s" or marker == "\s1"):
                u = UsfmS(marker, str(' '.join(words)))
            elif (marker == "\id"):
                # \id MAT <other text may appear here>
                self.id = words.pop(0)
                u = UsfmId(marker, self.id, str(' '.join(words)))
            else:
                u = Usfm(marker, "", str(' '.join(words)))

            self.usfms.append(u)

            #while words:
                #word = words.pop(0)
                # To find a single USFM marker, use the following (usual case):
                #markerMatch = markerPatternCompiled.search(word)
                #if (markerMatch != None): # word is a USFM marker

                # But lines sometimes have multiple markers, so have to loop through:
                #for markerMatch in regex.finditer(markerPatternCompiled, word):
                    #usfmCode = markerMatch.group(1)
                    #print(f"Marker {usfmCode}")
                    #count = markerDB.get(usfmCode, 0)
                    #markerDB[usfmCode] = count + 1;
                
        # Close the file
        file.close()
    
    def listParagraphs(self) -> str:
        # Return a json-string of a list of all paragraph marker locations, specified by the verse
        # /after/ the paragraph marker.
        plist = []
        chapter = 0
        for idx, u in enumerate(self.usfms):
            if (isinstance(u, UsfmP)):
                nextu = self.usfms[idx+1]
                if (not isinstance(nextu, UsfmV)):
                    print(f'WARNING: USFM after \p is not \v in {self.id} {chapter}')
                verse = nextu.number
                #print(f'{self.id} {chapter}:{verse}')
                # Store in list of tuples
                plist.append((self.id, int(chapter), int(verse)))

            # Keep track of chapter number
            if (isinstance(u, UsfmC)):
                chapter = u.number

        # Save the list
        #print(plist)
        return (json.dumps(plist, separators=(',', ':'))) # encode the json string

    def removeParagraphs(self):
        # My first list comprehension: assign to a slice which is my existing
        # list, and to get each new u, I walk each old u in the pre-existing 
        # usfsms list and if it is not a paragraph UsfmP type, then I take it.
        self.usfms[:] = [u for u in self.usfms if not isinstance(u, UsfmP)]

    def applyParagraphs(self, json_plist: str):
        # Given a list formatted by listParagraphs (above), we apply that 
        # paragraph structure to this book. It requires that you
        # run removeParagraphs on this book BEFORE this routine.
        plist = json.loads(json_plist) # decode the json string
        for (id, ch, vs) in plist:
            pass # WORK ON THIS

    def print(self):
        for u in self.usfms:
            u.print()

class Bible:
    def __init__(self, BibleName):
        self.name = BibleName
        # Bible contains a list of books
        self.books = []

    def printInternals(self):
        print(f'Data for {self.name}')
        for book in self.books:
            print(type(book))
            book.printInternals()

    def printname(self):
        print(self.name)

    def load(self):
        pass

    def loadBook(self, FileName):
        book = Book(FileName)
        book.load(FileName)
        self.books.append(book)

    def printBible(self, FileName):
        # USe FileName later
        for book in self.books:
            book.print()

def main():
    print("This is the USFM library; you cannot run it on its own!")

if __name__ == '__main__':
    main()
