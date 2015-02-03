const maxFileSizeKb = 100;

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

function SetupShortcutUploadBox(div, b, handler) {
    var handler_func = function (e) {
        FileSelectHandler(e, handler);
      }
  
    b[0].addEventListener(
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
      successHandler
    );
}

function UploadDraggedShortcutFiles(e, successFunction) {
	// fetch FileList object
	var files = e.target.files || e.dataTransfer.files;

	// Create a new FormData object.
	var formData = new FormData();
	
	// Loop through each of the selected files.
	var count = 0;
	var badExtensionCount = 0;
	var tooBigCount = 0;
	for (var i = 0; i < files.length; i++) {
	  var file = files[i];

	  // Check the file type.
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