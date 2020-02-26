#!/usr/bin/perl
$lastln = "";
$lastLnMatched = 0;
$lnNo = 0;
while ($ln = <>) {
    $lnNo++;
        # Look at the current line to look for " 4:27" like lines
	if (($ln =~ /^\s+[0-9]+:[0-9]+/) &&
	    ($lastLnMatched == 1)) {
	    # We have a match with this line and the previous
	    print "\\p";  # And no newline; rest will print below
	}
        elsif ($lastLnMatched == 1) {
	    # We matched a \p with nothing else on the line,
	    # thought it might be one of interest to us, but
	    # it was not. So, we have to print it out so it doesn't
	    # get "lost."
	    print "\\p\n"; # Newline = next print is a new line!
	}
    
	if ($ln =~ /^\\p$/) {
	    # Maybe going to be a match the next line
	    #print "Match could be coming [$lnNo]: $ln";
	    $lastLnMatched = 1;
	    # Don't print it yet
	}
	else {
	    $lastLnMatched = 0;
	    print $ln;
	}
	$lastln = $ln;
    }
