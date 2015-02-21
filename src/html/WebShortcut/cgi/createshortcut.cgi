#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use constant BUFFER_SIZE => 4096;

use utf8;

use lib 'lib';

use Archive::Zip qw( :ERROR_CODES :CONSTANTS );
use Archive::Tar;

use CGI qw/:all/;

use XML::DOM;

use HTML::Entities;

use File::Temp qw/ tempdir /;

use WebShortcutUtil::Write qw(
        create_desktop_shortcut_filename
        create_url_shortcut_filename
        create_webloc_shortcut_filename
        write_desktop_shortcut_handle
        write_url_shortcut_handle
        write_webloc_binary_shortcut_handle
        write_desktop_shortcut_file
        write_url_shortcut_file
        write_webloc_binary_shortcut_file);

# Returns routines and info for the specified shortcut type
sub get_shortcut_type_info {
  my ( $shortcut_type ) = @_;
 
  if($shortcut_type eq "url") {
    return (\&create_url_shortcut_filename,
            \&write_url_shortcut_file,
            \&write_url_shortcut_handle,
            "text/x-url");
  } elsif($shortcut_type eq "desktop") {
    return (\&create_desktop_shortcut_filename,
            \&write_desktop_shortcut_file,
            \&write_desktop_shortcut_handle,
            "application/x-desktop");
  } elsif($shortcut_type eq "webloc") {
    return (\&create_webloc_shortcut_filename,
            \&write_webloc_binary_shortcut_file,
            \&write_webloc_binary_shortcut_handle,
            "application/x-webloc");

  } else {
    die "Invalid shortcut type $shortcut_type";
  }
}

# Gets the name and URL from the XML "shortcut" node.
sub get_shortcut_node_info {
  my ($shortcut_node) = @_;

  my $name = $shortcut_node->getElementsByTagName ("name")->item(0)->getFirstChild->getNodeValue;
  my $url = $shortcut_node->getElementsByTagName ("url")->item(0)->getFirstChild->getNodeValue;

  return ($name, $url);
}


# Print a message to the error log.  It seems like if we die,
# no message will be printed if we do not print this line first???
eval {
print STDERR "convertshortcut.cgi starting...\n";

# Set upper limit on file size
$upload_limit_kb = 100;
$CGI::POST_MAX = 1024 * $upload_limit_kb;

my $query = CGI->new();

# Get the target shortcut type and associated info
my $shortcut_type = $query->param("target_shortcut_type");
my ($create_filename, $write_shortcut_file, $write_shortcut_handle, $mime_type) = get_shortcut_type_info($shortcut_type);

# Get the XML message with the names and URLs
my $xmldata = $query->param("xmldata");

# Get the type of archive to output - options are "none" (just give the new shortcut file directly)
# and "zip" (zip up the shortcuts).  If "none" is specified onyl the first shortcut in the XML will be
# created (there is no way to download multiple files without archiving them).
my $archive_type = $query->param("archive_type");

# Start parsing the XML - get the root "shortcuts" node.
my $parser = new XML::DOM::Parser;
my $doc = $parser->parse($xmldata);
my $shortcuts_node = $doc->getElementsByTagName ("shortcuts")->item(0);

if($archive_type eq "none") {
    # Get the first "shortcut" node and extract its name and URL.
    my $shortcut_node = $shortcuts_node->getChildNodes->item (0);
    my ($shortcut_name, $shortcut_url) = get_shortcut_node_info($shortcut_node);

    # Create a file name based on the name.  This should trim out any offending characters
    # (although if the name is based on an existing shortcut file name, then it should be
    #  clean anyway).
    my $shortcut_filename = &$create_filename($shortcut_name);

    # Start printing to the output.
    # Print the header.
    print "Content-Type:$mime_type\n";
    print "Content-Disposition:attachment;filename=\"$shortcut_filename\"\n\n";

    # Print the shortcut file
    binmode(STDOUT);
    &$write_shortcut_handle(\*STDOUT, $shortcut_name, $shortcut_url);
} elsif ($archive_type eq "zip") {
  # Get a temporary folder where we can build the zip file contents
  # We assume the temporary folder will be deleted automatically
  # when the script exits.
  my $global_tmp_dir = $ENV{'DOCUMENT_ROOT'} . "/../tmp";
  my $tmp_dir = tempdir( CLEANUP => 1, DIR => $global_tmp_dir );
  my $zip_contents_dir = $tmp_dir . "/zip";
  mkdir($zip_contents_dir);

  # Start creating the zip file structure.
  my $zip = Archive::Zip->new();

  # Go through all of the shortcuts in the XML message.
  foreach my $shortcut_node ($shortcuts_node->getChildNodes()) {
    # Get name and URL for the current shortcut
    my ($shortcut_name, $shortcut_url) = get_shortcut_node_info($shortcut_node);

    # Create the shortcut file name (this should strip out any dangerous
    # path separators / and \).
    my $shortcut_filename = &$create_filename($shortcut_name);

    # If the file name already exists append a "(#)" string to it and try
    # again.  Keep increment the number and trying until we succeed.
    my $counter = 1;
    my $new_shortcut_filename = $shortcut_filename;
    while(-e $zip_contents_dir . '/' . $new_shortcut_filename) {
      $new_shortcut_filename = $shortcut_filename . " ($counter)";
      $counter = $counter + 1;
    }
    $shortcut_filename = $new_shortcut_filename;

    # Create the path and then create the shortcut
    my $shortcut_full_filename = $zip_contents_dir . '/' . $shortcut_filename;
    &$write_shortcut_file($shortcut_full_filename, $shortcut_name, $shortcut_url);

    # Add the file to the zip file.  Inside the zip file, put it into a "shortcuts" folder.
    $zip->addFile($shortcut_full_filename, 'shortcuts/' . $shortcut_filename);
  }

  # Write the zip file
  my $zip_filename = $tmp_dir . "/shortcuts.zip";
  unless ( $zip->writeToFileNamed($zip_filename) == AZ_OK ) {
    die 'Error writing the zip file';
  }

  # Send the zip file to the client
  # Print the header
  print "Content-Type:application/zip\n";
  print "Content-Disposition:attachment;filename=\"shortcuts.zip\"\n\n";

  # Open the zip file and start sending it
  binmode(STDOUT);
  open my $zip_file,$zip_filename  or die "Cannot open file";
  binmode($zip_file);
  my $buffer = "";
  while ( read( $zip_file, $buffer, BUFFER_SIZE ) ) {
    print $buffer;
  }
  close $zip_file;
}

};
# Handle errors - just print a simple message in an HTML page.
if($@) {
  print STDERR "There was an error";
  my $error_message = encode_entities($@);
  print "Content-Type:text/html\n\n";
  print "<html><body><h1>An error has occurred:</h1>$error_message</body></html>";
}
