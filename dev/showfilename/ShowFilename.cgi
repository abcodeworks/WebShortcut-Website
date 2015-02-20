#!/usr/bin/perl

use utf8;

use Encode;
use CGI qw/:all/;

my $query = CGI->new();

print "Content-type: text/plain\n\n";

print "Here are the uploaded filenames:\n";

my @shortcut_files = $query->upload("shortcuts[]");
foreach my $shortcut_file (@shortcut_files) {
  #my $decoded_shortcut_file = decode(utf8=>$shortcut_file);
  my $decoded_shortcut_file = Encode::decode_utf8($shortcut_file);
  print STDOUT $shortcut_file . "\n";
  print STDOUT $decoded_shortcut_file . "\n";
  $shortcut_file =~ s/[x{0080}-\x{FFFF}]/_/g;
  print STDOUT $shortcut_file . "\n";
  $decoded_shortcut_file =~ s/[x{0080}-\x{FFFF}]/_/g;
  print STDOUT $decoded_shortcut_file . "\n";
}

#my @shortcut_files2 = $query->param("shortcuts[]");
#foreach my $shortcut_file (@shortcut_files2) {
#  my $decoded_shortcut_file = decode(utf8=>$shortcut_file);
#  print STDOUT $shortcut_file . "\n";
#  print STDOUT $decoded_shortcut_file . "\n";
#}