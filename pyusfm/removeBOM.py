import usfm;
import click
import os.path

# Remove the byte-order-mark (ef bb bf for UTF-8)
# and rewrite the file. Side effect: also changes
# the line endings from CRLF (Windows) to LF only.

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        print("Usage: python3 removeBOM.py *.txt")
        exit(1)

    for filename in files:
        if (os.path.exists(filename)):
            s = open(filename, mode='r', encoding='utf-8-sig').read()
            open(filename+".nobom", mode='w', encoding='utf-8').write(s)

if __name__ == '__main__':
    main()