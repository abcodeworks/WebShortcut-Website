#!/usr/bin/perl

# Reference: http://www.sitepoint.com/uploading-files-cgi-perl/

use lib 'lib';

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


# Print a message to the error log.  It seems like if we die,
# no message will be printed if we do not print this line first???
eval {
print STDERR "convertshortcut.cgi starting...\n";

my $query = CGI->new();
my $shortcut_type = $query->param("target_shortcut_type");
my $xmldata = $query->param("xmldata");

my $archive_type = $query->param("archive_type");
if($archive_type eq "none") {
  #print "<?xml version=\"1.0\" encoding=\"UTF-8\"?><shortcuttype>$shortcut_type</shortcuttype>";
# See http://www.perlmonks.org/?node_id=62809 for XML tips
    my $parser = new XML::DOM::Parser;
    my $doc = $parser->parse($xmldata);
    my $nodes = $doc->getElementsByTagName ("shortcuts");
    my $node = $nodes->item (0);
#    print STDERR $nodes->getLength;
    my $shortcutnodes = $node->getChildNodes;
#    print STDERR $shortcutnodes->getLength;
    my $shortcutnode = $shortcutnodes->item (0);
    my $name = $shortcutnode->getElementsByTagName ("name")->item(0)->getFirstChild->getNodeValue;
#    my $namenode = $shortcutnode->getElementsByTagName ("name");
#    print STDERR $namenode->getLength;
    my $url = $shortcutnode->getElementsByTagName ("url")->item(0)->getFirstChild->getNodeValue;
#    print STDERR "$name $url";
   # my $node = $nodes->item (1);
   # print STDERR $node->getValue . "\n";

#    my $name = "name";
#    my $url = "url";

    #$name =~ s/,//;
    #print STDERR $name;

    my ($create_filename, $write_shortcut_file, $write_shortcut_handle, $mime_type) = get_shortcut_type_info($shortcut_type);
    my $filename = &$create_filename($name);
    print "Content-Type:$mime_type\n";
    print "Content-Disposition:attachment;filename=\"$filename\"\n\n";
    &$write_shortcut_handle(\*STDOUT, $name, $url);
} else {
  # Start printing the output xml
  print "Content-type: text/xml\n\n";
  printf $xmldata;
}

};
if($@) {
  print STDERR "There was an error";
  my $error_message = encode_entities($@);
  print "Content-Type:text/html\n\n";
  print "<html><body><h1>An error has occurred:</h1>$error_message</body></html>";
}
