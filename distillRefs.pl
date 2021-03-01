#!/usr/bin/perl

# This takes input from USFM and extracts the refs and finds all the
# ways that books are referred to. This helps us to find errors in
# \toc3 entries so that Scripture App Builder can know the correct
# references. An unintended side-effect is that it also helps find
# inconsistent ways that books are referenced (1 Sam versus I Sam,
# for example), and wrong spacings. 

# Do a grep first to extract just the lines we want, and run
# like this:
# grep '\\r' *.usfm | ../../usfmtools/distillRefs.pl
# The grep allows us to be a little sloppy below, not checking for
# blank lines or lines with no interesting USFM like \r or \rq...\rq*

# First use for Rito NT. 
# Then adapted for Quechua which had a slightly different reference
# style (periods after book names, and some other peculiarities.

# Update 8/19/2020: encountered new usfm \rem, which starts with \r
# and affects the parser below.

# Update 11/11/2020: encountered \r 8-12 and similar references
# that do work in the SAB-generated app, but I flag as an error.
# See distillTest1.txt. 

# Update 2/27/2021: Trying to fix the "empty book" problem when 
# there is a book like "1 Kings." Test with
# cat distillTest.sfm | ./distillRefs.pl

$DEBUG = 0;

while ($ln = <>) {
    # Strip leading filename (if using grep, it is like 40_Matthew.usfm)
    $ln =~ s/^.+\.usfm://;
    $ln =~ s/^.+\.SFM://;
    # If a comment line, skip entirely
    if ($ln =~ /^\\rem/) { next; }
    if ($DEBUG) { print $ln; }
    # Strip leading \r, leading and trailing \rq...\rq*, parentheses
    $ln =~ s/.*\\r //;
    $ln =~ s/.*\\rq //;
    $ln =~ s/\\rq.*$//;
    $ln =~ s/\(//g;
    $ln =~ s/\)//g;
    $ln =~ s/\n$//g;
    $ln =~ s/\r$//g;
    # Strip multiple spaces in a row
    $ln =~ s/\s{1,}/ /g;
    # If there is a case of digit-space-digit, we are about to squash
    # out that space, and it will create a false reading. That would be
    # the case, say, if a cross ref was like Romans 8:28 29 instead of 8:28,29
    if ($ln =~ /[\d]\s+[\d]/) {
        print "Here is a cross-ref that seems wrong: ", $ln, "\n";
    }
    # Remove spaces
    $ln =~ s/([\*,;])\s+/$1/g;
    @refs = split('[\*,;]', $ln);
    if ($DEBUG) { print join('^^', @refs), "\n"; }
    if ($DEBUG) { print "Finding new verse refs in $ln\n"; }
    foreach $ref (@refs) {
        if ($DEBUG) { print "  ==>Reference:", $ref, "<== \n"; }
        if ($ref eq "") { 
            if ($DEBUG) { print "     Skipping blank\n"; }
            next;
        }
        # The references are in the format Tekikaga 20:13 (Rito NT)
        # So I need to extract the book name, and leave the rest.
        $ref =~ /(.+)\s+[0-9]/;
        # This will carry over to future loop iterations for like Jn. 1:1-2, 14
        $book = $1;
        if ($DEBUG) { print "  ==>Book:", $book, "<==\n"; }
        $books{$book}++; # record

        if ($book =~ /^\s+/) {
            print $ln, " has a book with a space at the beginning of the name\n";
        }

        if ($book eq "") {
            print $ln, " has an empty book\n";
            print "Previous line: ", $lastln, "\n\n";
        }
        elsif ($book eq "-") {
            print $ln, " has a mal-formed book\n";
            print "Previous line: ", $lastln, "\n\n";
        }
    }
    $lastln = $ln;
    $book = "";
    #print "\n";
}

printf("%-15s %s\n", "Book", "Occurrences");
printf("%-15s %s\n", "--------------", "-----------");
$totalxRefCount = 0;
foreach $book (sort keys %books) {
    printf("%-15s %d\n", $book, $books{$book});
    $totalxRefCount += $books{$book};
}

print "Number of variations = ", scalar keys %books, "\n";
print "Number of total xrefs = ", $totalxRefCount, "\n";

