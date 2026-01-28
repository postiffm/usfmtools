import usfm;
import click
import os.path

# This uses the usfm.py module. 
# What it does is load all the SFM files
# you give it, but combine the lines of them
# as per the needs of the Makusi project. Scan + OCR 
# + hand edits result in a file that looks like this:
#
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

    bibl = usfm.Bible("TestBible")

    for filename in files:
        if (os.path.exists(filename)):
            bibl.loadBook(filename)
            bk = bibl.lastBook()
            bk.combineLines()
            #bibl.printInternals()
            # And turn right around and print it
            f = open(filename+".new", "w")
            bk.print(f)

if __name__ == '__main__':
    main()