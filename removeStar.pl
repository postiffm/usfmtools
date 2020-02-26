#!/usr/bin/perl

# Try to first find all words that are marked with a *. This is
# commonly used by translators to indicate a glossary word. It is not
# correct USFM. * should be removed, or word should be surrounded by
# \w ... \w* USFM.

# Usage: removeStar *.SFM

sub replaceStar {
    my $fni = shift(@_);
    my $fno = shift(@_);
    open (my $fhi, "<", $fni);
    open (my $fho, ">", "$fno");

    while ($ln = <$fhi>) {
	@parts = split(/\s+/, $ln);
	#print @parts;
	foreach $part (@parts) {
	    #print $part, " ";
	    if (($part =~ /\s*\\qt\*\s*/) ||
		($part =~ /\s*\\xt\*\s*/) ||
		($part =~ /\s*\\f\*\s*/) ||
		($part =~ /\s*\\w\*\s*/) ||
		($part =~ /\s*\\qt\*\s*/)) {
		# Ignore certain parts that end with \*...they are fine
		print $fho $part, " ";
	    }
	    elsif ($part =~ /\*/) {
		#print "Candidate to fix? ::: ", $part, "\n";
		@subparts = split(/\*/, $part);
		#print "Candidate to fix? ::: \\w $subparts[0] \\w*$subparts[1] ", "\n";
		print $fho "\\w $subparts[0] \\w*$subparts[1] ";
	    }
	    else {
		# An uninteresting part
		print $fho $part, " ";
	    }
	    #elsif ($part =~ /\\c/) { print $part, " "; }
	    #elsif ($part =~ /\\v/) { print $part, " "; }
	    #elsif ($part =~ /\[0-9]+/) { print $part, " "; }
	}
	print $fho "\n";
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
    replaceStar($filenamebak, $filename);
}
