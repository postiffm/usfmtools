import usfm;
import click
import os.path

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

@click.command()
@click.argument('files', nargs=-1)
def main(files):
    if (len(files) == 0):
        print("Usage: python3 checkMarkers.py bible")
        exit(1)

    # Fill in here

if __name__ == '__main__':
    main()

