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

#use XML::Writer;

use WebShortcutUtil::Write qw(
        create_desktop_shortcut_filename
        create_url_shortcut_filename
        write_desktop_shortcut_handle
        write_url_shortcut_handle);

# Print a message to the error log.  It seems like if we die,
# no message will be printed if we do not print this line first???
print STDERR "convertshortcut.cgi starting...\n";

my $query = CGI->new();
my $shortcut_type = $query->param("target_shortcut_type");


my $archive_type = $query->param("archive_type");
if($archive_type eq "none") {
  #print "<?xml version=\"1.0\" encoding=\"UTF-8\"?><shortcuttype>$shortcut_type</shortcuttype>";
#  if($shortcut_type eq "url") {
    my $filename = create_url_shortcut_filename("my");
    print STDERR $filename;
    #print "Content-Type:application/x-desktop";    application/x-webloc
    print STDOUT "Content-Type:text/x-url\n";
    print STDOUT "Content-Disposition:attachment;filename=$filename\n\n";
    #$io = IO::Handle->new();
    #$io->fdopen(fileno(STDOUT),"w");
    #write_desktop_shortcut_handle($io, "My Name", "http://google.com");
    write_url_shortcut_handle(\*STDOUT, "My Name", "http://google.com");
#  } elsif($shortcut_type eq "desktop") {
#  } elsif($shortcut_type eq "webloc") {
#  } else {
#    die "Invalid shortcut type $shortcut_type";
#  }
} else {
  # Start printing the output xml
  print "Content-type: text/xml\n\n";

  my $xmldata = $query->param("xmldata");

  printf $xmldata;
}
