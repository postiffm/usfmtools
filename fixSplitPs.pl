#!/usr/bin/perl

# Find all occurrences like this in Sara Ngam NT:
# \p 
#  4:27
# I found one, for example, in 44JHNNgam.SFM around line 235.
# I need to fix these before running removeHeaderRefs because
# it looks for lines like \p 1:11 to remove.

# Usage: fixSplitPs *.SFM

# Again, a problem with newlines. I run it in the test.pl script, and it is fine.
# I put it in here, and the newline thing goes crazy. What I do to solve this
# is strip out \r\n in the first line of the while loop, and then add "\n" wherever
# needed to fix the fact that I removed all the existing \n, so need to add them back.

sub fixSplitPs {
    my $fni = shift(@_);
    my $fno = shift(@_);
    open (my $fhi, "<", $fni);
    open (my $fho, ">", "$fno");

    $lastln = "";
    $lastLnMatched = 0;
    $lnNo = 0;

    while ($ln = <$fhi>) {
	$ln =~ s/[\r\n]+//g;
	$lnNo++;
        # Look at the current line to look for " 4:27" like lines
	if (($ln =~ /^\s+[0-9]+:[0-9]+/) &&
	    ($lastLnMatched == 1)) {
	    # We have a match with this line and the previous
	    print $fho "\\p";  # And no newline; rest will print below
	}
        elsif ($lastLnMatched == 1) {
	    # We matched a \p with nothing else on the line,
	    # thought it might be one of interest to us, but
	    # it was not. So, we have to print it out so it doesn't
	    # get "lost."
	    print $fho "\\p\n"; # Newline = next print is a new line!
	}
    
	if ($ln =~ /^\\p$/) {
	    # Maybe going to be a match the next line
	    #print "Match could be coming [$lnNo]: $ln";
	    $lastLnMatched = 1;
	    # Don't print it yet
	}
	else {
	    $lastLnMatched = 0;
	    print $fho $ln, "\n";
	}
	$lastln = $ln;
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
    fixSplitPs($filenamebak, $filename);
}
