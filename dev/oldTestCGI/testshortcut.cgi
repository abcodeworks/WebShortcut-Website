#!/usr/bin/perl

use CGI qw(:standard);
use lib 'lib';
use WebShortcutUtil::Write qw(
        create_desktop_shortcut_filename
        create_url_shortcut_filename
        create_webloc_shortcut_filename
        write_desktop_shortcut_file
        write_url_shortcut_file
        write_webloc_binary_shortcut_file
        write_webloc_xml_shortcut_file);

my $filename = create_desktop_shortcut_filename("Shortcut: Name");
print "Content-type: text/html\n\n";
print "Greetings user.\n"; 
print "$filename\n";
