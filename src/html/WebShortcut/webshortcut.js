function GetFileExtension(filename) {
  var a = filename.split(".");
  if( a.length === 1 || ( a[0] === "" && a.length === 2 ) ) {
    return "";
  }
  return a.pop();
}

function ProcessDraggedShortcutFiles(e, successFunction, failFunction) {
	// fetch FileList object
	var files = e.target.files || e.dataTransfer.files;

	// Create a new FormData object.
	var formData = new FormData();
	
	// Loop through each of the selected files.
	var count = 0, skipCount = 0;
	for (var i = 0; i < files.length; i++) {
	  var file = files[i];

	  // Check the file type.
	  var fileExtension = GetFileExtension(file.name);
	  if (fileExtension != 'url' &&
	      fileExtension != 'website' &&
	      fileExtension != 'desktop' &&
	      fileExtension != 'webloc') {
	    skipCount++;
	    continue;
	  }

	  // Add the file to the request.
	  formData.append('shortcuts[]', file, file.name);
	  count++;
	}

  if(skipCount > 0) {
    window.alert("Some files did not have a valid extension and are being ignored");
  }
 
	if(count == 0) {
	  return;
	} 
	
  $.ajax({
    url: GetParseShortcutUrl(),
    data: formData,
    cache: false,
    contentType: false,
    processData: false,
    type: 'POST',
    success: successFunction,
    error: failFunction
  });
}