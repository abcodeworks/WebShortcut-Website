#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use constant BUFFER_SIZE => 4096;

use lib 'lib';

use Archive::Zip qw( :ERROR_CODES :CONSTANTS );
use Archive::Tar;

use CGI qw/:all/;

# Note that we do not use CGI::Carp -
# I would like to create my own handler which outputs an error XML, but
# I get an error that set_die_handler is not exported.
# So, if there is an error in this main routine, the user will not be aware
# what happened.  However, if there is an error parsing the shortcut, then
# this should be handled properly below, and the user should get an error message
# for each file.

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

sub get_shortcut_info {
  my ($shortcut_node) = @_;

  my $name = $shortcut_node->getElementsByTagName ("name")->item(0)->getFirstChild->getNodeValue;
  my $url = $shortcut_node->getElementsByTagName ("url")->item(0)->getFirstChild->getNodeValue;

  return ($name, $url);
}


# Print a message to the error log.  It seems like if we die,
# no message will be printed if we do not print this line first???
eval {
print STDERR "convertshortcut.cgi starting...\n";

my $query = CGI->new();

my $shortcut_type = $query->param("target_shortcut_type");
my ($create_filename, $write_shortcut_file, $write_shortcut_handle, $mime_type) = get_shortcut_type_info($shortcut_type);

my $xmldata = $query->param("xmldata");

my $archive_type = $query->param("archive_type");

my $parser = new XML::DOM::Parser;
my $doc = $parser->parse($xmldata);
my $shortcuts_node = $doc->getElementsByTagName ("shortcuts")->item(0);

if($archive_type eq "none") {
  #print "<?xml version=\"1.0\" encoding=\"UTF-8\"?><shortcuttype>$shortcut_type</shortcuttype>";
# See http://www.perlmonks.org/?node_id=62809 for XML tips
#    my $node = $nodes->item (0);
#    print STDERR $nodes->getLength;
    #my $shortcutnodes = $node->getChildNodes;
#    print STDERR $shortcutnodes->getLength;
    my $shortcut_node = $shortcuts_node->getChildNodes->item (0);
    my ($shortcut_name, $shortcut_url) = get_shortcut_info($shortcut_node);
#    print STDERR "$name $url";
   # my $node = $nodes->item (1);
   # print STDERR $node->getValue . "\n";

#    my $name = "name";
#    my $url = "url";

    #$name =~ s/,//;
    #print STDERR $name;

    my $shortcut_filename = &$create_filename($shortcut_name);
    print "Content-Type:$mime_type\n";
    print "Content-Disposition:attachment;filename=\"$shortcut_filename\"\n\n";
    binmode(STDOUT);
    &$write_shortcut_handle(\*STDOUT, $shortcut_name, $shortcut_url);
} else {
  # Start printing the output xml
  #print "Content-type: text/xml\n\n";
  #printf $xmldata;
  my $global_tmp_dir = $ENV{'DOCUMENT_ROOT'} . "/../tmp";
  my $tmp_dir = tempdir( CLEANUP => 1, DIR => $global_tmp_dir );
#  print STDERR $tmp_dir;

  my $zip_contents_dir = $tmp_dir . "/zip";
  mkdir($zip_contents_dir);

#  my $zip = Archive::Zip->new();
  my $zip = Archive::Tar->new;
  foreach my $shortcut_node ($shortcuts_node->getChildNodes()) {
    my ($shortcut_name, $shortcut_url) = get_shortcut_info($shortcut_node);
    my $shortcut_filename = &$create_filename($shortcut_name);

    my $counter = 1;
    my $new_shortcut_filename = $shortcut_filename;
    while(-e $zip_contents_dir . '/' . $new_shortcut_filename) {
      $new_shortcut_filename = $shortcut_filename . " ($counter)";
      $counter = $counter + 1;
    }
    $shortcut_filename = $new_shortcut_filename;

    my $shortcut_full_filename = $zip_contents_dir . '/' . $shortcut_filename;
    &$write_shortcut_file($shortcut_full_filename, $shortcut_name, $shortcut_url);
    #$zip->addFile($shortcut_full_filename, 'shortcuts/' . $shortcut_filename);
    $zip->add_files($shortcut_full_filename);
    $zip->rename($shortcut_full_filename, 'shortcuts/' . $shortcut_filename);
  }

#  open(my $uploadfh, ">", "$zip_contents_dir/myfile.txt");
#  print $uploadfh "Hello World";
#  close($uploadfh);

#  print STDERR "$zip_contents_dir/myfile.txt";

#  my $zip_filename = $tmp_dir . "/download.zip";
#  unless ( $zip->writeToFileNamed($zip_filename) == AZ_OK ) {
#    die 'write error';
#  }
  my $zip_filename = $tmp_dir . "/download.tar.gz";
  $zip->write($zip_filename, COMPRESS_GZIP);

  # See http://docstore.mik.ua/orelly/linux/cgi/ch13_02.htm"
  print "Content-Type:application/zip\n";
#  print "Content-Disposition:attachment;filename=\"shortcuts.zip\"\n\n";
  print "Content-Disposition:attachment;filename=\"shortcuts.tar.gz\"\n\n";


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
if($@) {
  print STDERR "There was an error";
  my $error_message = encode_entities($@);
  print "Content-Type:text/html\n\n";
  print "<html><body><h1>An error has occurred:</h1>$error_message</body></html>";
}
