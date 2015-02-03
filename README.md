WebShortcut-Website
===================

Web Shortcut Tools website

Pel
---
See https://support.godaddy.com/help/article/293/do-i-need-to-change-the-permissions-to-files-in-my-cgi-directory
To make the PERL scripts executable:
  chmod 705 file
OR to change all files in the current directory
  chmod -R 705 .

Development
-----------
To run on a local machine, use the server.js file from the dev folder.
To allow for cross-site scripting, close all Chrome windows, and then run Chrome as follows:

  Linux: google-chrome --disable-web-security
  Windows: "C:\Program Files (x86)\Google\Chrome\Application\chrome" --disable-web-security

The dev folder contains various helper utilities.
  
Testing
-------
The following unit tests should be run:
- More tests to come...
- Make sure file extensions are checked.
- Make sure file sizes are limited.
- Verify the files int he lib folder ar enot executed:
  For example: http://abcodeworks.com/cgi/lib/WebShortcutUtil.pm