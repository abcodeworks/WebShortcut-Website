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

use XML::Writer;

use WebShortcutUtil::Read qw(
        get_handle_reader_for_file);

# Print a message to the error log.  It seems like if we die,
# no message will be printed if we do not print this line first???
print STDERR "parseshortcut.cgi starting...\n";

# Set upper limit on file size
$upload_limit_kb = 100;
$CGI::POST_MAX = 1024 * $upload_limit_kb;


# Start printing the output xml
print "Content-type: text/xml\n\n";
my $query = CGI->new();

foreach $line ( <STDIN> ) {
    chomp( $line );
    print "$line\n";
}