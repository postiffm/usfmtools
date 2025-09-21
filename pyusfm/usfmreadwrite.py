import usfm;
import click
import os.path

# Following is an example of how to use the usfm.py
# module. What it does is load all the SFM files
# you give it, print it back out to a set of new files,
# list out the paragraph locations, and then remove
# all the paragraph markers.

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        print("Usage: python3 usfmreadwrite.py *.usfm")
        exit(1)

    b = usfm.Bible("TestBible")

#    markerDB = {}
    for filename in files:
        if (os.path.exists(filename)):
            b.loadBook(filename)
            # And turn right around and print it

    #b.printBible(filename+".new")
    #b.printInternals()

    for book in b.books:
        plist = book.listParagraphs() # print a list of all paragraph marker locations
        print(plist)
        book.removeParagraphs() # remove all \p markers

    #b.printBible(filename+".new")

if __name__ == '__main__':
    main()

a# 1. I would like to write another code that does this
# Usage: applyparagraphs.py bible1 bible2
# What it does: take paragraphing from bible1 and apply 
# it to bible2 (first removing existing paragraphs from 
# bible2).
# We need to extend what usfm.py can do, and be able to
# write very nice looking code in applyparagraphs.py
# that uses that api.
# I am thinking:
# b1 = usfm.Bible("bible1")
# b2 = usfm.Bible("bible2")
# b1.load(directory1) # bible::load routine loads all SFM files in directory1
# b2.load(directory2)
# b2.removeParagraphs() # code already done
# paragraphs = b1.listParagraphs() # draft code already done
# b2.applyParagraphs(paragraphs) # new stuff
# b2.printBible(directory2.new) # draft code done, but needs debugged
# This will be super helpful because we have translations with no paragraphing.
# I would like to find a nicely paragraphed bible and quickly apply its 
# paragraphing to the "bad" Bible.

# 2. I would like to write another code that dumps all our paragraphing:
# foreach bible in <all of several folders>
#   b = usfm.Bible("blah")
#   paragraphs = b.listParagraphs()
#   print paragraphs
#   but we have to figure out what format to print them so that we can 
#   then somehow understand them. json might not be the best
#   so maybe we need a pretty-print method
#   like:
# Genesis
#     1:1
#     1:5
#     ...
# Exodus
#     1:1
#     ...

# 3. I would also like a simple script checkMarkers.py
#    for marker in approvedMarkerDB:
#       print(f"{marker}\t{markerDB[marker]}", end='')
#       if (not (marker in ApprovedMarkers)):
#            print("\t<<== This marker is not in the BI approved list")
#        else:
#            print("")
# I have something like that already in findMarkers.py
# but it would be nice to neatly integrate that into the usfm.py
# module. Of course, our "approved markers" will differ from other
# people because Bibles International has its own "tribal custom"
# but that's OK. We are working for them and can always adjust the
# approved list later.

# These are just three projects. The ultimate goal is to 
# keep doing projects whereby we can expand the functionality 
# of the usfm.py library and use it for many more things in 
# the future.