#!/usr/bin/perl

# Find any \v that are not starting a new line in the given files
my @files = @ARGV;
print "Files: ", join(' ', @files), "\n";
my $totalFinds = 0;
foreach my $f (@files) {
    $totalFinds += findInFile($f);
}
print STDERR "Found total of $totalFinds mistakes in placement of \v USFM marker\n";

sub findInFile {
    my $f = shift(@_);
    my $found = 0;
    print "Processing $f...";
    open(my $fh, "<", $f) || return 0; # die "Can't open < $f: $!";
    while ($ln = <$fh>) {
	if ($ln =~ /.+\\v/) {
	    #print "$f: misplaced \v: $ln";
	    $found++;
	}
    }
    print "Found $found times\n";
    return $found;
}
