var upload_form = $("#upload_form")
if(upload_form) {
    upload_form.attr("action", GetParseShortcutUrl());
}

function GetParseShortcutUrl() {
  return 'http://abcodeworks.com/cgi/parseshortcut.cgi';
}

function GetCreateShortcutUrl() {
  return 'http://abcodeworks.com/cgi/createshortcut.cgi';
}