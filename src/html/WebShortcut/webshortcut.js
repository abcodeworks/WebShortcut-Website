function GetFileExtension(filename) {
  var a = filename.split(".");
  if( a.length === 1 || ( a[0] === "" && a.length === 2 ) ) {
    return "";
  }
  return a.pop();
}

function htmlEncode(value) {
    return $('<div/>').text(value).html();
}

function SetupShortcutUploadBox(div, form, handler) {
    form[0].addEventListener("change", FileSelectHandler, false);

    div.addClass("shortcutupload_box");
    div[0].addEventListener("dragover", FileDragOver, false);
    div[0].addEventListener("dragleave", FileDragLeave, false);
    div[0].addEventListener(
      "drop",
      function (e) {
        FileSelectHandler(e, handler);
      },
      false);
    div[0].style.display = "block";
}

// file drag hover
function FileDragOver(e) {
    e.stopPropagation();
    e.preventDefault();
    $(e.target).addClass("hover");

    $(e.target).children().addClass('inactive');

}

function FileDragLeave(e) {
    e.stopPropagation();
    e.preventDefault();
    $(e.target).removeClass("hover");

    $(e.target).children().removeClass('inactive');
}

// file selection
function FileSelectHandler(e, successHandler) {

    // cancel event and hover styling
    FileDragLeave(e);

    UploadDraggedShortcutFiles(
      e,
      successHandler,
      function (xhr, ajaxOptions, thrownError) {
          alert('An error occurred submitting the shortcuts to the server: status=' + xhr.status + ' error=' + thrownError);
      }
    );
}

function UploadDraggedShortcutFiles(e, successFunction, failFunction) {
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

    // ADD CHECK FOR FILE SIZE

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