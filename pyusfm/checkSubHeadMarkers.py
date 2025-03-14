import usfm;
import click
import os.path

# This uses the usfm.py module. 
# Run through all .SFM files we are given, and find out if 
# there are sequences like this:
# \s1
# \c
# because they need to be swapped to be correct. You cannot have
# a \s# header at the END of a chapter. It must be at the top of
# the next chapter.

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        # __file__
        print(f"Usage: python3 {os.path.basename(__file__)} *.SFM")
        exit(1)

    bibl = usfm.Bible("TestBible")

    for filename in files:
        if (os.path.exists(filename)):
            print(f"{filename}")
            bibl.loadBook(filename)
            # If running fixSubHeads, rename file to backup
            #os.rename(filename, filename+".bak")
            bk = bibl.lastBook()
            bk.checkSubHeads()
            #f = open(filename, "w")
            #bk.print(f)
            #f.close()
        else:
            print(f"ERROR: Cannot find {filename}")

if __name__ == '__main__':
    main()