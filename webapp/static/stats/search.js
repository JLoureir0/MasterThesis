const attributes = JSON.parse(document.getElementById('attributes').textContent);


window.onload = function() {
    var waitingDialog = waitingDialog || (function ($) {
	'use strict';

	// Creating modal dialog's DOM
	var $dialog = $(
	    '<div class="modal fade" data-backdrop="static" data-keyboard="false" tabindex="-1" role="dialog" aria-hidden="true" style="padding-top:15%; overflow-y:visible;">' +
		'<div class="modal-dialog modal-m">' +
		'<div class="modal-content">' +
		'<div class="modal-header"><h3 style="margin:0;"></h3></div>' +
		'<div class="modal-body">' +
		'<div class="progress progress-striped active" style="margin-bottom:0;"><div class="progress-bar" style="width: 100%"></div></div>' +
		'</div>' +
		'</div></div></div>');

	return {
	    /**
	     * Opens our dialog
	     * @param message Custom message
	     * @param options Custom options:
	     * 				  options.dialogSize - bootstrap postfix for dialog size, e.g. "sm", "m";
	     * 				  options.progressType - bootstrap postfix for progress bar type, e.g. "success", "warning".
	     */
	    on: function(a,b) {
		$dialog.on(a,b);
	    },
	    show: function (message, options) {
		// Assigning defaults
		if (typeof options === 'undefined') {
		    options = {};
		}
		if (typeof message === 'undefined') {
		    message = 'Loading';
		}
		var settings = $.extend({
		    dialogSize: 'm',
		    progressType: '',
		    onHide: null // This callback runs after the dialog was hidden
		}, options);

		// Configuring dialog
		$dialog.find('.modal-dialog').attr('class', 'modal-dialog').addClass('modal-' + settings.dialogSize);
		$dialog.find('.progress-bar').attr('class', 'progress-bar');
		if (settings.progressType) {
		    $dialog.find('.progress-bar').addClass('progress-bar-' + settings.progressType);
		}
		$dialog.find('h3').text(message);
		// Adding callbacks
		if (typeof settings.onHide === 'function') {
		    $dialog.off('hidden.bs.modal').on('hidden.bs.modal', function (e) {
			settings.onHide.call($dialog);
		    });
		}
		// Opening dialog
		$dialog.modal();
	    },
	    /**
	     * Closes dialog
	     */
	    hide: function () {
		$dialog.modal('hide');
	    }
	};

    })(jQuery);

    $("#search-input").keypress(function(e){
	if(e.which == 13) {
	    waitingDialog.show();
	}
    });
    
    waitingDialog.on('shown.bs.modal', function(){
	search($("#search-input").val());
    });

    $("#search-button").click(function(e){
	waitingDialog.show();
    });

    function search(input) {
	const search_result = fuzzysort.go(input, attributes);

	var search_content = $("#search-content");

	search_content.html("");

	for(var i = 0; i < search_result.length; i++) {
	    search_content.html(search_content.html() + '<li class="list-inline-item"><a href="' + window.location.href + '/' + search_result[i]['target'] + '">' + search_result[i]['target'] + '</a></li>');
	}
	
	waitingDialog.hide();
    }
}
