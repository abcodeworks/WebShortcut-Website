#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use lib 'lib';

use CGI qw/:all/;

use CGI::Carp;
#BEGIN {
#   sub handle_errors {
#     my $msg = shift;
#
#     print "Content-type: text/xml\n\n";
#
#     my $writer = XML::Writer->new(ENCODING => 'utf-8');
#     $writer->dataElement("error", $msg);
#     $writer->end();
# }
# CGI:Carp::set_die_handler(\&handle_errors);
#}

use File::Temp qw/ tempfile tempdir /;

use XML::Writer;

use WebShortcutUtil::Read qw(
        get_handle_reader_for_file);

print STDERR "parseshortcut.cgi starting...\n";

$upload_limit_kb = 100;
$CGI::POST_MAX = 1024 * $upload_limit_kb;


print "Content-type: text/xml\n\n";

my $query = CGI->new();

my $writer = XML::Writer->new(ENCODING => 'utf-8');
$writer->startTag("shortcuts");

die "my error";

my @shortcut_files = $query->upload("shortcuts[]");
foreach my $shortcut_file (@shortcut_files) {
  $writer->startTag("shortcut");
  $writer->dataElement("filename", $shortcut_file);

  my $url = "";
  eval {
    my $reader = get_handle_reader_for_file($shortcut_file);
    $url = &$reader($shortcut_file);
  };

  if($@) {
    $writer->dataElement("error", $@);
  } else {
    $writer->dataElement("name", $shortcut_file);
    $writer->dataElement("url", $url);
  }

  $writer->endTag("shortcut");
}

$writer->endTag("shortcuts");
$writer->end();
