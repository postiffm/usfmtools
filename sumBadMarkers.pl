#!/usr/bin/perl

# Take input like this:
#x	13	<<== This marker is not in the BI approved list
#x*	13	<<== This marker is not in the BI approved list
#x	14	<<== This marker is not in the BI approved list
#x*	14	<<== This marker is not in the BI approved list
#x	22233	<<== This marker is not in the BI approved list
#x*	22233	<<== This marker is not in the BI approved list
#x	4213	<<== This marker is not in the BI approved list
#x*	4213	<<== This marker is not in the BI approved list
#xo	13	<<== This marker is not in the BI approved list
#xo	22233	<<== This marker is not in the BI approved list
#xo	4213	<<== This marker is not in the BI approved list

# and add up all the marker counts to summarize.

while ($ln = <>) {
    @parts = split('\t', $ln);
    #print $ln;
    $marker = $parts[0];
    $count = $parts[1];
    $msg = $parts[2];
    $markerCount{$marker} += $count;
    #print $marker, "\t", $count, "\n";
}

foreach $marker (sort keys %markerCount) {
    print $marker, "\t", $markerCount{$marker}, "\n";
}