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
        # I have to re-constitute the content
        if (self.marker != ""):
            print(f'{self.marker}')
        if (self.arg != ""):
            print(f'{self.arg}')
        if (self.content != ""):
            print(f'{self.content}')

    def append(self, usfmObject):
        #print("ADDING CONTENT ", end="")
        #usfmObject.print()
        if (usfmObject.marker != ""):
            print("ERROR: attempting to append USFM beginning with marker; unanticipated case: ", end="")
            usfmObject.print()
        else:
            #print("BEFORE ADDING, CONTENT=", end="")
            #self.print()
            self.content = self.content + " " + usfmObject.content
            #print("AFTER ADDING,  CONTENT=", end="")
            #self.print()

# Specialized classes for specific USFM markers
class UsfmC(Usfm):
    # \c #
    def __init__(self, Marker, Number, ):
        super().__init__(Marker, Number, "")
        self.arg = Number # \c X, arg X is the chapter number
    def print(self):
        print(f'{self.marker} {self.arg}')

class UsfmP(Usfm):
    # \p (paragraph marker)
    def __init__(self, Marker="p", Content=""):
        super().__init__(Marker, "", Content)
    def print(self):
        print(f'{self.marker}')
        if (self.content != ""):
            print(f'{self.content}')
            # Not really sure why a \p line should have anything else on it...

class UsfmV(Usfm):
    # \v # verse text
    def __init__(self, Marker, Number, Text):
        super().__init__(Marker, Number, Text)
        self.arg = Number # \v X, where X is the verse number
        self.content = Text
    def print(self):
        print(f'{self.marker} {self.arg} {self.content}')

class UsfmS(Usfm):
    # \s# Heading
    def __init__(self, Marker, Heading):
        super().__init__(Marker, "", Heading)
        self.heading = Heading
    def print(self):
        print(f'{self.marker} {self.heading}')

class UsfmH(Usfm):
    # \h Heading
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self):
        print(f'{self.marker} {self.content}')

class UsfmTOC(Usfm):
    # \toc# content
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self):
        print(f'{self.marker} {self.content}')

class UsfmMT(Usfm):
    # \mt# content
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self):
        print(f'{self.marker} {self.content}')

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
            print(type(u), end="")
            print(" :: ", end="")
            u.print()

    def load(self, FileName):
        """Reads in the entire USFM and stores it in our nascent data model"""
        # Be aware of there is a BOM in the file, \id will not match properly
        # Need to more gracefully handle that situation. Until then, use removeBOM.py
        # to clean the BOM out of the file.
        file = open(FileName,'r')
        for line in file:
            # Ignore blank lines
            if not line.strip():
                continue;

            words = line.split()
            # Get the first marker
            u = ""
            marker = words.pop(0)
            #print(f'MARKER = ::{marker}::')
            if (marker == "\\v"):  # Must escape the backslash in each of these checks
                u = UsfmV(marker, words.pop(0), str(' '.join(words)))
            elif (marker == "\c"):
                u = UsfmC(marker, words.pop(0))
            elif (marker == "\p"):
                u = UsfmP(marker, str(' '.join(words)))
            elif (marker == "\\s" or marker == "\\s1" or marker == "\\s2"):
                u = UsfmS(marker, str(' '.join(words)))
            elif (marker == "\\h"):
                u = UsfmH(marker, str(' '.join(words)))
            elif (marker == "\\toc1" or marker == "\\toc2" or marker == "\\toc3"):
                u = UsfmTOC(marker, str(' '.join(words)))
            elif (marker == "\\mt" or marker == "\\mt1" or marker == "\\mt2" or marker == "\\mt3"):
                u = UsfmMT(marker, str(' '.join(words)))
            elif (marker == "\\id"):
                # \id MAT <other text may appear here but probably should not>
                self.id = words.pop(0)
                u = UsfmId(marker, self.id, str(' '.join(words)))
                #print("New ID Marker: ", end="")
                #u.print()
            elif (marker[0] == "\\"):
                # There is some other marker here, but I don't specifically care what it is
                self.arg = words.pop(0)
                u = Usfm(marker, self.arg, str(' '.join(words)))
                #print("New UNKNOWN Marker: ", end="")
                #u.print()
            else:
                # There is apparently no marker on this line. Not a really nice USFM line, but what we have
                # Prepend the marker back into the word list
                words = [marker] + words
                u = Usfm("", "", str(' '.join(words)))
                #print("New GENERIC USFM: ", end="")
                #u.print()

            self.usfms.append(u)

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

    def combineLines(self):
        # This came from the Makusi project where scan+OCR+manual correct
        # resulted in a file that had lines that needed combined.
        newu = [] # Since we have to remove lines, just build a new list of usfms
        for idx, u in enumerate(self.usfms):
            #u.print()
            if (isinstance(u, UsfmC) or 
                isinstance(u, UsfmP) or 
                isinstance(u, UsfmS) or
                isinstance(u, UsfmV) or
                isinstance(u, UsfmId) or
                isinstance(u, UsfmH) or
                isinstance(u, UsfmTOC) or
                isinstance(u, UsfmMT)):
                # Do nothing but append the USFM to our new list
                # It should not be followed by an non-marker line
                newu.append(u)
            else: # This line is not one of the above types; likely does not start w/ a marker
                if (u.marker != ""):
                    print("ERROR: Unanticipated case: ", end="")
                    u.print()
                else: # The line does not start with a marker, so append to end of prior
                    #print(f"{u.marker} {u.arg} {u.content}")
                    # If you get an index out of range error here, twice it has been because the 
                    # file has a byte-order mark at the beginning before the \id marker. Remove that
                    # with python3 ../../usfmtools/pyusfm/removeBOM.py and you should be all set.
                    newu[-1].append(u)
                    newu[-1].content = newu[-1].content.replace("- ", "")
        # Now update the final USFM
        self.usfms = newu

    def print(self, FileName):
        #file = open(FileName,'w')
        # use FileName later
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

    def lastBook(self):
        return self.books[-1]

    def print(self, FileName):
        for book in self.books:
            book.print(FileName)

def main():
    print("This is the USFM library; you cannot run it on its own!")

if __name__ == '__main__':
    main()
