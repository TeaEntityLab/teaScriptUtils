#!/usr/bin/perl -w
# Perl script to convert HTML files to DokuWiki Markup.
# Requires HTML::WikiConverter Perl module

use HTML::WikiConverter;

print "HTML to DokuWiki markup converter\n";
my $argcnt = $#ARGV + 1;
if ($argcnt == 2) {
	print "Converting...";
	my $infile = "$ARGV[0]";
	my $outfile= "$ARGV[1]";
	use Shell qw(html2wiki);
	$ENV{'WCDIALECT'} = 'DokuWiki';
	html2wiki ("$infile > $outfile");
	open FILE, ">$outfile" or die $!;		
	while (<FILE>) {
		printf $_;
	}
	close FILE;
	print "done.\nYour DokuWiki article is now available in $outfile.\n";
}
	else {
		print "Usage: html2doku input.html output.txt\n";
		
}

