#!/usr/bin/perl

use CGI qw/:all/;

my $query = CGI->new();

# Get the XML message with the names and URLs
my $xmldata = $query->param("xmldata");

print "Content-type: text/xml\n\n";
print STDOUT $xmldata;
print STDERR $xmldata;
