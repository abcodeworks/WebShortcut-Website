#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use utf8;

use lib 'lib';

use Encode;

use CGI qw/:all/;

# Note that we do not use CGI::Carp -
# I would like to create my own handler which outputs an error XML, but
# I get an error that set_die_handler is not exported.
# So, if there is an error in this main routine, the user will not be aware
# what happened.  However, if there is an error parsing the shortcut, then
# this should be handled properly below, and the user should get an error message
# for each file.

# I also considered adding an eval around the main body and returning an
# xml file with error information.  However,
# we start printing to the output fairly early in this script.
# And I think that once we print the header we cannot then go back and
# send a different header and xml message.  We could process the uploaded
# files and cache the results, then print them later, but I think this
# complicates things and uses more memory.  Hopefully, we won't see a lot of
# errors here (besides shortcut parsing errors which should already be caught
# and passed back to the client int he xml message)...

use XML::Writer;

use WebShortcutUtil::Read qw(
        get_handle_reader_for_file
        get_shortcut_name_from_filename);

# Print a message to the error log.  It seems like if we die,
# no message will be printed if we do not print this line first???
print STDERR "parseshortcut.cgi starting...\n";

# Set upper limit on file size
# This does not appear to work?  It seems like the file is uploaded
# immediately.  I will leave it here, though - maybe it works
# under some circumstances.
$upload_limit_kb = 1000;
$CGI::POST_MAX = 1024 * $upload_limit_kb;

my $query = CGI->new();

my $remove_unicode_from_filename = $query->param("remove_unicode_from_filename");
my @shortcut_files = $query->upload("shortcuts[]");

# Start printing the output xml
print "Content-type: text/xml\n\n";

my $writer = XML::Writer->new(ENCODING => 'utf-8');
$writer->startTag("shortcuts");

# Go through each uploaded file, parse, and output results
foreach my $shortcut_file (@shortcut_files) {
  $writer->startTag("shortcut");

  my $shortcut_filename = decode(utf8=>$shortcut_file);
  if($remove_unicode_from_filename eq "yes") {
    $shortcut_filename =~ s/[x{0080}-\x{FFFF}]/_/g;
  }
  $shortcut_filename = $shortcut_filename . $remove_unicode_from_filename;
  $writer->dataElement("filename", $shortcut_filename);

  my $name = get_shortcut_name_from_filename($shortcut_filename);
  $writer->dataElement("name", $name);

  # Try parsing the file - if the routine dies, put the error
  # message into the xml.
  my $url = "";
  eval {
    my $reader = get_handle_reader_for_file($shortcut_file);
    $url = &$reader($shortcut_file);
  };

  if($@) {
    $writer->dataElement("error", $@);
  } else {
    $writer->dataElement("url", $url);
  }

  $writer->endTag("shortcut");
}

$writer->endTag("shortcuts");
$writer->end();
