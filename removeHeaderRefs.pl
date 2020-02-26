#!/usr/bin/perl

# Find all occurrences like this in Sara Ngam NT:
# \p 1:11
# \p (Mise 5:1)
# Anna Beth Wivell reports that the first case were running headers
# left in by the people who put the text into Paratext. It concerned
# page layout in the print version and is not right.
# The second case is an example of a cross-ref that should be a \r
# instead of a \p.

# Problem: I was seeing this script INTRODUCE ^M carriage returns into
# the output when they were NOT there in the original source .SFM files.
# I did not understand this. Some files had and some did not.
# The issue was in part that 0d0a line endings were present in the original,
# but Emacs was not visually showing it. Strange.
# To make everything work right, I had to add
# $ln =~ s/[\r\n]+//g;
# at the beginning of the loop to clear out everything offending,
# and then put a \n at the end of every line as I want it.
#
# Something was also messed up in the pattern match, but I got rid of $ 
# at the end of them, and that works better.

# After doing this, I found another case that needs attention:
# \p
#  4:27
# in 44JHNNgam.SFM
# around line 235. There were quite a few of these in there.
# Need to figure out what to do

# Usage: removeHeaderRefs *.SFM

sub removeHeaderRefs {
    my $fni = shift(@_);
    my $fno = shift(@_);
    open (my $fhi, "<", $fni);
    open (my $fho, ">", "$fno");

    while ($ln = <$fhi>) {
	$ln =~ s/[\r\n]+//g;
	if ($ln =~ /^\\p [0-9]+:[0-9]+\s*/) {
	    #print "This looks suspicious, remove: $ln\n";
	    # Do not print it
	}
	elsif ($ln =~ /^\\p (\([\w\.]+\s[0-9]+:[0-9]+\))\s*/) {
	    #print "This looks like it could be \\r: $ln\n";
	    print $fho "\\r $1\n";
	}
	else {
	    print $fho "$ln\n";
	}
    }
    close($fhi);
    close($fho);
}

## MAIN ##
# Tip: to do a mass rename, do this:
# rename 's/\.bak$//' *.bak
# This removes .bak from every filename.bak file

foreach $filename (@ARGV) {
    print "Processing $filename\n";

    $filenamebak = "$filename.bak";

    # rename the file to .bak
    if (!rename ($filename, $filenamebak)) {
	die "Cannot backup $filename : $!";
	exit(1);
    }

    # Now put the contents of the backup (original) file into the
    # new file, but with the transformation requested.
    removeHeaderRefs($filenamebak, $filename);
}
