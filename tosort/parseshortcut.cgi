#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use CGI qw/:all/;

use CGI::Carp qw ( fatalsToBrowser set_message );
# For now leave a blank error message (the default gives a bad email address).
set_message("test");

use File::Temp qw/ tempfile tempdir /;

use lib 'lib';
use WebShortcutUtil::Read qw(
        read_shortcut_file);

$upload_limit_kb = 100;
$CGI::POST_MAX = 1024 * $upload_limit_kb;

print "Content-type: text/html\n\n";

my $query = CGI->new();
@names = $query->param;
print("Params:");
foreach my $filename (@names) {
  print "Param: $filename\n";
}

$tmp_dir = $ENV{'DOCUMENT_ROOT'} . "/../tmp";

@names2 = $query->param("shortcuts[]");
foreach my $filename2 (@names2) {
  print "$filename2\n";
     #foreach my $f (@file){
     #while (($n = read $f, $data, 10000000, $size) != 0) {
     #$r = $data;
     #}

}

print $ENV{'DOCUMENT_ROOT'}; 

$dir = tempdir( CLEANUP => 1, DIR => $tmp_dir );
print("Temp dir: $dir\n");


#my $shortcut_files1 = query->upload('shortcuts');

my @shortcut_files2 = $query->upload("shortcuts[]");
foreach my $shortcut_file (@shortcut_files2) {
  print "$shortcut_file\n";
}

#

#foreach my $file (@shortcut_files) {
#  print "$file\n";
#}

#my $filename = create_desktop_shortcut_filename("Shortcut: Name");

print "Greetings user.\n"; 
#print "$filename\n";
