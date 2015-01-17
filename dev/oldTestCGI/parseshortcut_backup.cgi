#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use CGI qw/:all/;

use CGI::Carp qw ( fatalsToBrowser set_message );
# For now leave a blank error message (the default gives a bad email address).
set_message("test");

use File::Temp qw/ tempfile tempdir /;

use lib 'lib';
use WebShortcutUtil::Read qw(
        get_handle_reader_for_file);

$upload_limit_kb = 100;
$CGI::POST_MAX = 1024 * $upload_limit_kb;

print "Content-type: text/html\n\n";

my $query = CGI->new();
@names = $query->param;
print("Params:");
foreach my $filename (@names) {
  print "Param: $filename<br/>";
}

#$tmp_dir = $ENV{'DOCUMENT_ROOT'} . "/../tmp";
#$dir = tempdir( CLEANUP => 1, DIR => $tmp_dir );
#print("Temp dir: $dir<br/>");


@names2 = $query->param("shortcuts[]");
foreach my $filename2 (@names2) {
  print "$filename2<br/>";
}

my @shortcut_files = $query->upload("shortcuts[]");
foreach my $shortcut_file (@shortcut_files) {
  print "$shortcut_file<br/>";

  #($uploadfh, $uploadfilename) = tempfile(DIR => $dir, SUFFIX => ".desktop", UNLINK => 0);
# open(my $uploadfh, ">", "$tmp_dir/myfiles.txt"); 
  #print("Temp file: $uploadfilename<br/>");

#while ( <$shortcut_file> )
 #{
 #print $uploadfh $_;
 #}

#close $uploadfh;
  print "$shortcut_file<br/>";

  my $reader = get_handle_reader_for_file($shortcut_file);

  my $url = &$reader($shortcut_file);
  
  print "$url<br/>";
}

#

#my $filename = create_desktop_shortcut_filename("Shortcut: Name");

print "Greetings user.\n"; 
#print "$filename\n";
