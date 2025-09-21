import os
import bible


def OutPutVerse(strverse: str) -> str:
    # Function definition to put the encoded verse into xml format
    strverse = "      <Verse>" + strverse + "</Verse>"
    return strverse


def ConvertToUSFMSpelling(strbook: str) -> str:
    # Function definition to convert the first three letters of the book into USFM ID when not the same as the 1st three letters
    if strbook == "SON":
        strbook = "SNG"
    elif strbook == "EZE":
        strbook = "EZK"
    elif strbook == "JOE":
        strbook = "JOL"
    elif strbook == "NAH":
        strbook = "NAM"
    elif strbook == "MAR":
        strbook = "MRK"
    elif strbook == "JOH":
        strbook = "JHN"
    elif strbook == "1JO":
        strbook = "1JN"
    elif strbook == "2JO":
        strbook = "2JN"
    elif strbook == "3JO":
        strbook = "3JN"
    return strbook


def CheckReferenceValidity(strbook: str, strchapter: str, strverse: str) -> str:
    # Function definition to evaluate the reference to ensure it is valid before doing the word of encoding and including in the output
    strReturnMessage = "UNTESTED"
    IsValid = bible.checkChapterInRange(strbook, int(strchapter))
    if IsValid == True:
        IsValid = bible.checkVerseInRange(
            strCurrentBook, int(strChapterNumber), int(StrVerseNumber))
        if IsValid == False:
            strReturnMessage = "ERROR-Verse"
        else:
            strReturnMessage = "VERIFIED"
    else:
        strReturnMessage = "ERROR-Chapter"
    return strReturnMessage


def LogErrorMessages(strpath: str, strmessage: str):
    # Function to log error messages
    logfile = open(strpath, "a")  # append mode
    logfile.write(strmessage + "\n")
    logfile.close()


strlogfile = "C:\\BibleTrans\\RobOut\\4-YofHosts-ErrorOutput.txt"
outputfile = "C:\\BibleTrans\\RobOut\\4-YOH-python.txt"
NewVerseIndicator = "NKJ"  # This is the Bible version and is found at the beginning of the chapter and verse reference - indicates a new book and chapter combination - otherwise it's just a number
DocContent = open(
    'C:\\BibleTrans\\RobOut\\4-YofHosts-NoHeader.txt', 'r').read()  # This is a text file where Word document output was copied without the header / gloss info - just verses
# Splitting into a list based on new line character - Could try \n\n since usually double newlines, but went with single in case there is inconsistency and just check for empty lines
strLines = DocContent.split("\n")
strCurrentBook = "NONE"  # Will be used to track current book which will be critical when the reference is only a number - in that case use this to know the book/chapter
# Same as current book - used when the reference is only a number
strCurrentChapter = "00"
# This is a list that is built and then used to write the full output - built one verse code at a time
StrVerseCodeList = []
# First line of the file is the References XML - manually gets pasted inside of header/footer xml info
StrVerseCodeList.append("    <References>")
strChapterNumber = "000"
StrVerseNumber = "000"
# Looping through each line of the file to extract reference info to encode
for l in range(len(strLines)):
    StrBookTemp = ""
    TrimLine = strLines[l]
    if len(TrimLine) > 5:  # Checking this to ensure it is not an empty line
        # Converting to uppercase to do the USFM Book ID lookup which is based on uppercase
        TrimLine = TrimLine.strip().upper()
        # Looking for the Bible version reference which indicates a new book & chapter is included in the reference instead of verse only
        if TrimLine.startswith(NewVerseIndicator):
            # Removing the version info so we can extract the book name for the USFM ID lookup
            TrimLine = TrimLine.replace(NewVerseIndicator, "")
            # removes empty/whitespace at beginning and end of the line
            TrimLine = TrimLine.strip()
            # Get Book and Chapter as it is found here
            # Step 1 - Look for space in second spot - this means 1,2,3 books
            if TrimLine[1] == " ":
                # Rebuild the line without the space as the codes don't have the space in them
                StrBookTemp = TrimLine[0] + TrimLine[2] + TrimLine[3]
                # Adding the remainder of the line after having removed the space
                TrimLine = StrBookTemp + TrimLine[4:]
            else:
                # No space found - so get the first 3 letters of the book
                StrBookTemp = TrimLine[0:3]
            # Step 2 - Find duplicate spelling start books: 1) JUD - Jude or Judges???  2) PHI - Philemon or Philippians
            # Converting book first three letters to USFM IDs - so for the duplicates handle those - otherwise send to the function to convert
            if StrBookTemp == "JUD":
                if TrimLine[0:5] == "JUDG":
                    StrBookTemp = "JDG"
            elif StrBookTemp == "PHI":
                if TrimLine[0:5] == "PHILE":
                    StrBookTemp = "PHM"
                else:
                    StrBookTemp = "PHP"
            else:
                # Sending these to the function to convert the ones that have a USFM ID different than the first few letters of the actual name - e.g., SNG for Song of Solomon or MRK for Mark
                StrBookTemp = ConvertToUSFMSpelling(StrBookTemp)
            strCurrentBook = StrBookTemp
            # Now get Chapter
            strArr = TrimLine.split(" ")
            # Chapter:Verse will be second index - but it's zero based therefore using 1
            strIndex = strArr[1].split(":")
            strChapterNumber = strIndex[0]
            StrVerseNumber = strIndex[1]
        else:
            # This was not a book and chapter reference - so we re-use book and chapter and simply obtain verse
            strArr = TrimLine.split(" ")
            StrVerseNumber = strArr[0].strip()  # Verse will be first index
            # Need to do this because we converted to lowercase for refEncode to work - but this will cause error on usfmIDToBook lookup if not upper
            strCurrentBook = strCurrentBook.upper()

        # Error handling for errors - catch them and log them
        bookFound = True
        try:
            StrBookTemp = bible.usfmIDToBook.get(strCurrentBook)
        except:
            bookFound = False  # Error on Book name
        if (bookFound == True) and (StrBookTemp is not None):
            # Before encoding - check validity of the reference
            strCurrentBook = StrBookTemp
            strValidity = CheckReferenceValidity(
                strCurrentBook, strChapterNumber, StrVerseNumber)
            if strValidity == "VERIFIED":
                strWholeVerseCode = bible.refEncode(
                    strCurrentBook, int(strChapterNumber), int(StrVerseNumber))
                strWholeVerseCode = OutPutVerse(strWholeVerseCode)
                StrVerseCodeList.append(strWholeVerseCode)
            else:
                # Determine if it was due to chapter or verse or untested
                if strValidity == "UNTESTED":
                    strlogmessage = "Error - could not test reference"
                elif strValidity == "ERROR-Chapter":
                    strlogmessage = "Error because did not find chapter {} as a valid chapter for the book of {} on line {}".format(
                        strChapterNumber, strCurrentBook, TrimLine)
                else:
                    strlogmessage = "Error because did not find verse {} as a valid verse for chapter {} in the book of {} on line {}".format(
                        StrVerseNumber, strChapterNumber, strCurrentBook, TrimLine)
                LogErrorMessages(strlogfile, strlogmessage)    # Log error
        else:
            strlogmessage = "Error because did not find book {} as a valid book in USFM ID codes on line {}".format(
                strCurrentBook, TrimLine)
            # Log error on book not found
            LogErrorMessages(strlogfile, strlogmessage)

StrVerseCodeList.append("    </References>")

with open(outputfile, 'w') as f:
    for item in StrVerseCodeList:
        f.write("%s\n" % item)
