#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use lib 'lib';


use CGI qw/:all/;

use CGI::Carp qw ( fatalsToBrowser set_message );
# For now leave a blank error message (the default gives a bad email address).
set_message("test");

use File::Temp qw/ tempfile tempdir /;

use XML::Writer;

use WebShortcutUtil::Read qw(
        get_handle_reader_for_file);

$upload_limit_kb = 100;
$CGI::POST_MAX = 1024 * $upload_limit_kb;

print "Content-type: text/xml\n\n";

my $query = CGI->new();
#@names = $query->param;
#print("Params:");
#foreach my $filename (@names) {
  #print "Param: $filename<br/>";
#}

#$tmp_dir = $ENV{'DOCUMENT_ROOT'} . "/../tmp";
#$dir = tempdir( CLEANUP => 1, DIR => $tmp_dir );
#print("Temp dir: $dir<br/>");


#@names2 = $query->param("shortcuts[]");
#foreach my $filename2 (@names2) {
#  print "$filename2<br/>";
#}

my $writer = XML::Writer->new(ENCODING => 'utf-8');

#print '<?xml version="1.0" encoding="UTF-8"?>';
#print "<shortcuts>";
$writer->startTag("shortcuts");

my @shortcut_files = $query->upload("shortcuts[]");
foreach my $shortcut_file (@shortcut_files) {
  #print "<shortcut>";
  #print "<filename>$shortcut_file</filename>";
  $writer->startTag("shortcut");
  $writer->dataElement("filename", $shortcut_file);

  #($uploadfh, $uploadfilename) = tempfile(DIR => $dir, SUFFIX => ".desktop", UNLINK => 0);
# open(my $uploadfh, ">", "$tmp_dir/myfiles.txt"); 
  #print("Temp file: $uploadfilename<br/>");

#while ( <$shortcut_file> )
 #{
 #print $uploadfh $_;
 #}

#close $uploadfh;
  #print "$shortcut_file<br/>";

my $url = "";
eval {
  my $reader = get_handle_reader_for_file($shortcut_file);
  $url = &$reader($shortcut_file);
};

if($@) {
#print "<error>$@</error>";
$writer->dataElement("error", $@);
} else {
 # print "<name>$shortcut_file</name>"; 
 # print "<url>$url</url>";
  $writer->dataElement("name", $shortcut_file);
  $writer->dataElement("url", $url);
}


  #print "<error>msg</error>";

 # print "</shortcut>";
  $writer->endTag("shortcut");

}

$writer->endTag("shortcuts");
$writer->end();
#print "</shortcuts>";

#

#my $filename = create_desktop_shortcut_filename("Shortcut: Name");

#print "Greetings user.\n"; 
#print "$filename\n";
