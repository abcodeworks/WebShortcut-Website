// Override form actions inside the html
var upload_form = $("#upload_form")
if(upload_form) {
    upload_form.attr("action", GetParseShortcutUrl());
}

var convert_form = $("#convert_form")
if(convert_form) {
    convert_form.attr("action", GetCreateShortcutUrl());
}

function GetParseShortcutUrl() {
  return 'http://abcodeworks.com/cgi/parseshortcut.cgi';
}

function GetCreateShortcutUrl() {
  return 'http://abcodeworks.com/cgi/createshortcut.cgi';
}