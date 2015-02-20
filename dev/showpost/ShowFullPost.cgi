#!/usr/bin/perl

use CGI qw(:standard);

print "Content-type: text/plain\n\n";

while(my $line = <STDIN>) {
  print STDOUT $line;
  print STDERR $line;
}