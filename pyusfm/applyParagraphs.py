import usfm;
import click
import os.path

# 1. I would like to write another code that does this
# Usage: applyParagraphs.py bible1 bible2
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

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        print("Usage: python3 applyParagraphs.py bible1 bible2")
        exit(1)

    # Fill in here

if __name__ == '__main__':
    main()
