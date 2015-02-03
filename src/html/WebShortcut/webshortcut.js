// HELPER FUNCTIONS
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




// UPLOAD DIV
// All that is required to initialize a div for shortcut upload
// is to call SetupShortcutUploadBox

// Initializes the specified div to be a drag box for
// uploading shortcuts.  The button should be attached
// to an upload form (used as an alternative to dragging)
// When shortcuts are uploaded,
// the handler is called with the results.
function SetupShortcutUploadBox(div, button, handler) {
  var handler_func = function (e) {
      FileSelectHandler(e, handler);
    }
  
  button[0].addEventListener(
    "change",
    handler_func,
    false);

  div.addClass("shortcutupload_box");
  div[0].addEventListener("dragover", FileDragOver, false);
  div[0].addEventListener("dragleave", FileDragLeave, false);
  div[0].addEventListener(
    "drop",
    handler_func,
    false);
  div[0].style.display = "block";
}

// Handler when file is dragged over the div
function FileDragOver(e) {
  e.stopPropagation();
  e.preventDefault();
  $(e.target).addClass("hover");

  // The drag will exit when the cursor enters
  // a child of the div.  To avoid this,
  // temporarily "inactivate" the children.
  // See http://stackoverflow.com/questions/7110353/html5-dragleave-fired-when-hovering-a-child-element
  //     http://stackoverflow.com/questions/10867506/dragleave-of-parent-element-fires-when-dragging-over-children-elements
  $(e.target).children().addClass('inactive');
}

// Handler when file is dragged out of the div
function FileDragLeave(e) {
    e.stopPropagation();
    e.preventDefault();
    $(e.target).removeClass("hover");

    $(e.target).children().removeClass('inactive');
}

// Handler when a file is selected or a file is dropped
function FileSelectHandler(e, successHandler) {

    // cancel event and hover styling
    FileDragLeave(e);

    UploadDraggedShortcutFiles(
      e,
      successHandler
    );
}

const maxFileSizeKb = 100;

// Check the files, upload, and get the response
function UploadDraggedShortcutFiles(e, successFunction) {
	var files = e.target.files || e.dataTransfer.files;

	var formData = new FormData();
	
	// Loop through each of the selected files.
	var count = 0;
	var badExtensionCount = 0;
	var tooBigCount = 0;
	for (var i = 0; i < files.length; i++) {
	  var file = files[i];

	  // Check the files for problems
	  var fileExtension = GetFileExtension(file.name);
	  if (fileExtension != 'url' &&
	      fileExtension != 'website' &&
	      fileExtension != 'desktop' &&
	      fileExtension != 'webloc') {
	    badExtensionCount++;
	    continue;
	  }
	  if(file.size > (maxFileSizeKb * 1024)) {
	    tooBigCount++;
	    continue;
	  }

	  // Add the file to the request.
	  formData.append('shortcuts[]', file, file.name);

	  count++;
	}

  if(badExtensionCount > 0) {
    window.alert("Some files did not have a valid extension and are being ignored");
  }
  
  if(tooBigCount > 0) {
    window.alert("Some files were larger than the maximum size of " + maxFileSizeKb + " kb and are being ignored");
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
    error: function (xhr, ajaxOptions, thrownError) {
        alert('An error occurred submitting the shortcuts to the server: status=' + xhr.status + ' error=' + thrownError);
      }
  });
}