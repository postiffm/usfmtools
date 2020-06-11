#!/usr/bin/perl

sub stripFootnotes {
    my $fni = shift(@_);
    my $fno = shift(@_);
    open (my $fhi, "<", $fni);
    open (my $fho, ">", "$fno");


    while ($ln = <$fhi>) {
	$ln =~ s/\\f.+\\f\*//g;
	print $fho $ln;
    }
}

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
    stripFootnotes($filenamebak, $filename);
}
