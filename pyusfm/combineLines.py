import usfm;
import click
import os.path

# This uses the usfm.py module. 
# What it does is load all the SFM files
# you give it, but combine the lines of them
# as per the needs of the Makusi project. OCR text
# and hand edits result in a file that 
# look like this:
#\v 1 Uurî Tiago wanî Paapa moropai Uyepotorîkon Jesus
#Cristo poitorî pe. Seni kaarita yarimauya judeuyamî pia
# and these need to be combined. Lines that end with -
# need to be combined specially--by deleting the - and
# removing whitespace.

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        print("Usage: python3 combineLines.py *.txt")
        exit(1)

    b = usfm.Bible("TestBible")

    for filename in files:
        if (os.path.exists(filename)):
            b.loadBook(filename)
            b.combineLines(filename)
            # And turn right around and print it

    b.printBible(filename+".new")
    b.printInternals()

if __name__ == '__main__':
    main()