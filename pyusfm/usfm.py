# USFM tools
# (c) Matt Postiff, 2022-2023
# Experimental coding project for USFM processing

import regex
import json
import sys

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

    def print(self, f=sys.stdout):
        # I have to re-constitute the content
        # This prints each part on a separate line which is incorrect
        if (self.marker != ""):
            print(f'{self.marker}', file=f)
        if (self.arg != ""):
            print(f'{self.arg}', file=f)
        if (self.content != ""):
            print(f'{self.content}', file=f)

    def append(self, usfmObject):
        #print("ADDING CONTENT ", end="")
        #usfmObject.print()
        if (usfmObject.marker != ""):
            print("ERROR: attempting to append USFM beginning with marker; unanticipated case: ", end="")
            usfmObject.print()
        else:
            #print("BEFORE ADDING, CONTENT=", end="")
            #self.print()
            #print("ADDITIONAL CONTENT via usfmObject.print=", end="")
            #usfmObject.print()
            #print("ADDITIONAL CONTENT via print usfmObject.content=", end="")
            #print(f"{usfmObject.content}")
            self.content = self.content + " " + usfmObject.content
            #print(f"{self.content}")
            #print("AFTER ADDING,  CONTENT=", end="")
            #self.print()

# Specialized classes for specific USFM markers
class UsfmC(Usfm):
    # \c #
    def __init__(self, Marker, Number, ):
        super().__init__(Marker, Number, "")
        self.arg = Number # \c X, arg X is the chapter number
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.arg}', file=f)

class UsfmP(Usfm):
    # \p (paragraph marker)
    # Followed immediately by a space and paragraph text, or by a new line and a verse marker.
    def __init__(self, Marker="p", Content=""):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        if (self.content != ""):
            print(f'{self.marker} {self.content}', file=f)
        else:
            print(f'{self.marker}', file=f)

class UsfmV(Usfm):
    # \v # verse text
    def __init__(self, Marker, Number, Text):
        super().__init__(Marker, Number, Text)
        self.arg = Number # \v X, where X is the verse number
        self.content = Text
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.arg} {self.content}', file=f)

class UsfmS(Usfm):
    # \s# Heading
    def __init__(self, Marker, Heading):
        super().__init__(Marker, "", Heading)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmH(Usfm):
    # \h Heading
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmTOC(Usfm):
    # \toc# content
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmMT(Usfm):
    # \mt# content
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmId(Usfm):
    # \id MAT <other text may appear here>
    def __init__(self, Marker, Id, Content):
        super().__init__(Marker, Id, Content)
        self.id = Id
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.id} {self.content}', file=f)

class UsfmM(Usfm):
    # \m text
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmR(Usfm):
    # \r text like 
    # \r (1,19-12,50) (or \mr after an \ms)
    # or 
    # \r (Mt 3,11-12; Mr 1,7-8; Nk 3,15-17) (after a \s1 line)
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmRq(Usfm):
    # \rq text like 
    # \rq Ezayii 66:24 \rq*
    # This is I think my first marker with a start and end marker
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
        self.endmarker="\\rq*"
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content} {self.endmarker}', file=f)

class UsfmQ(Usfm):
    # \q1 text
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmLi(Usfm):
    # \li1 text
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

class UsfmRem(Usfm):
    # \rem text, a comment
    def __init__(self, Marker, Content):
        super().__init__(Marker, "", Content)
    def print(self, f=sys.stdout):
        print(f'{self.marker} {self.content}', file=f)

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
            elif (marker == "\\c"):
                u = UsfmC(marker, words.pop(0))
            elif (marker == "\\p" or marker == "\\ip"):
                u = UsfmP(marker, str(' '.join(words)))
            elif (marker == "\\s" or marker == "\\s1" or marker == "\\s2"):
                u = UsfmS(marker, str(' '.join(words)))
            elif (marker == "\\h"):
                u = UsfmH(marker, str(' '.join(words)))
            elif (marker == "\\toc1" or marker == "\\toc2" or marker == "\\toc3"):
                u = UsfmTOC(marker, str(' '.join(words)))
            elif (marker == "\\mt" or marker == "\\mt1" or marker == "\\mt2" or marker == "\\mt3" or marker == "\\ms" or marker == "\\imt1"):
                u = UsfmMT(marker, str(' '.join(words)))
            elif (marker == "\\id"):
                # \id MAT <other text may appear here but probably should not>
                self.id = words.pop(0)
                u = UsfmId(marker, self.id, str(' '.join(words)))
                #print("New ID Marker: ", end="")
                #u.print()
            elif (marker == "\\q1" or marker == "\\q2" or marker == "\\q3" or marker == "\\q4"):
                u = UsfmQ(marker, str(' '.join(words)))
            elif (marker == "\\m"):
                u = UsfmM(marker, str(' '.join(words)))
            elif (marker == "\\r"):
                u = UsfmR(marker, str(' '.join(words)))
            elif (marker == "\\mr"):
                u = UsfmR(marker, str(' '.join(words)))
            elif (marker == "\\rq"):
                if (words[-1] == '\\rq*'):
                    words.pop()
                else:
                    print("ERROR: Did not find final \\rq* endmarker")
                u = UsfmRq(marker, str(' '.join(words)))
            elif (marker == "\\li1"):
                u = UsfmLi(marker, str(' '.join(words)))
            elif (marker == "\\rem"):
                u = UsfmRem(marker, str(' '.join(words)))
            elif (marker[0] == "\\"):
                print("New UNKNOWN Marker: ", marker)
                # There is some other marker here, but I don't specifically care what it is
                self.arg = words.pop(0) # this assumes it has an argument. It might not (blank \ip lines, which should not exist, but...)
                u = Usfm(marker, self.arg, str(' '.join(words)))
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
                    print(f'WARNING: USFM after \\p is not \\v in {self.id} {chapter}')
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
        # This originated with the Makusi project where scan+OCR+manual correct
        # resulted in a file that had lines that needed combined so that each
        # verse resides on a line of text (if no \m or \q1, for example)
        newu = [] # Since we have to remove lines, just build a new list of usfms
        for idx, u in enumerate(self.usfms):
            #print("Processing USFM >> ", end="")
            #u.print()
            if (isinstance(u, UsfmC) or 
                isinstance(u, UsfmP) or 
                isinstance(u, UsfmS) or
                isinstance(u, UsfmV) or
                isinstance(u, UsfmId) or
                isinstance(u, UsfmH) or
                isinstance(u, UsfmTOC) or
                isinstance(u, UsfmMT) or
                isinstance(u, UsfmR)):
                # Do nothing but append the USFM to our new list
                # It should not be followed by a non-marker line...this is a false statement...\s1 can be split across lines!
                newu.append(u)
            elif (isinstance(u, UsfmQ) or
                  isinstance(u, UsfmM)):
                # These markers start their own new line of USFM text
                #print("New USFM line with q1 or m marker")
                newu.append(u)
            else: # This line is not one of the above types; likely does not start with a marker
                if (u.marker != ""):
                    print("ERROR: Unanticipated case: ", end="")
                    u.print()
                else: # The line does not start with a marker, so append to end of prior
                    #print(f"INFO: {u.marker} {u.arg} {u.content}")
                    # If you get an index out of range error here, twice it has been because the 
                    # file has a byte-order mark at the beginning before the \id marker. Remove that
                    # with python3 ../../usfmtools/pyusfm/removeBOM.py and you should be all set.
                    newu[-1].append(u)
                    #newu[-1].content = newu[-1].content.replace("- ", "")   # Does not work right for -- sequence
                    #re.sub(pattern, replacement, string, count=0, flags=0)
                    # For lines that end with a dash (in Makusi and Wampis), we remove the - and combine the two word parts.
                    # They are hyphenated and in the USFM we need to get rid of the hyphen--and NOT the preceding character!
                    newu[-1].content = regex.sub("([^-])- ", "\\1", newu[-1].content)

                    # The below code never runs because \q1 markers are handled in the above elif. Hmmm.
                    # But there is also a common case where a hyphenated word is split with a \q1 marker also.
                    # The resulting combined string will be word- \q1 restofword and it should be combined
                    # into wordrestofword. The \q1 marker goes away entirely. This happens in a context where
                    # the prior line is also a \q1 marker. Our editors added too many \q1 markers to match
                    # the formatting of the printed page, but really only one \q1 marker should have been used.
                    #print(newu[-1].content)
                    #newu[-1].content = regex.sub("[^-]- \\\\q1 ", "", newu[-1].content)
        # Now update the final USFM
        self.usfms = newu

    def fixSubHeads(self):
        # This originated with the Kabiye project when we learned that it was
        # making the same mistake we had made elsewhere--putting \s1 before \c
        # which has to be swapped.
        # Run this AFTER combineLines has combined everything
        newu = [] # Since we have to swap lines, just build a new list of usfms
        for idx, u in enumerate(self.usfms):
            #print("Processing USFM >> ", end="")
            #u.print()
            if (isinstance(u, UsfmC)):
                # Check if preceding was a \s#. If so, print message and put this one
                # BEFORE that \s# line.
                if (isinstance(newu[-1], UsfmS)):
                    #print(f"line {idx+1}: \\c after \\s# in {u}")
                    sMarkeru = newu.pop()  # pop off the \s marker line
                    newu.append(u)         # push on the \c marker
                    u = sMarkeru           # prepare to push on the \s marker next
                # Append either the \c marker or the swapped out \s# marker from the if stmt
                newu.append(u)
            else:
                # Anything else just is just forwarded
                newu.append(u)

        # Now update the final USFM
        self.usfms = newu

    def print(self, f=sys.stdout):
        for u in self.usfms:
            u.print(f)

class Bible:
    def __init__(self, BibleName):
        self.name = BibleName
        # Bible contains a list of books
        self.books = []

    def printInternals(self, f=sys.stdout):
        print(f'Data for {self.name}', file=f)
        for book in self.books:
            print(type(book), file=f)
            book.printInternals()

    def printname(self, f=sys.stdout):
        print(self.name, file=f)

    def load(self):
        pass

    def loadBook(self, FileName):
        book = Book(FileName)
        book.load(FileName)
        self.books.append(book)

    def lastBook(self):
        return self.books[-1]

    def print(self, f=sys.stdout):
        for book in self.books:
            book.print(f)

def main():
    print("This is the USFM library; you cannot run it on its own!")

if __name__ == '__main__':
    main()
