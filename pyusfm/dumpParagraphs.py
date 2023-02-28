import usfm;
import click
import os.path

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
# And maybe a wrapper script around this, or this can handle multiple Bible folders as command-line arguments

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        print("Usage: python3 dumpParagraphs.py bible1")
        exit(1)

    # Fill in here

if __name__ == '__main__':
    main()
