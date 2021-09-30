$(document).ready(() => {
	// websockets
	const wsPath = 'ws://' + window.location.host + "/events";
	console.log("Connecting to " + wsPath);
	const webSocketBridge = new channels.WebSocketBridge();
	webSocketBridge.connect(wsPath);
	webSocketBridge.listen(function (data) {
		alert("Wow! New question " + data["title"] + " by " + data["author"])
	});

	// hide #back-top first
	$("#back-top").hide();
	
	// fade in #back-top
	$(function () {
		$(window).scroll(function () {
			if ($(this).scrollTop() > 100) {
				$('#back-top').fadeIn();
			} else {
				$('#back-top').fadeOut();
			}
		});
		// scroll body to 0px on click
		$('#back-top a').click(function () {
			$('body,html').animate({
				scrollTop: 0
			}, 800);
			return false;
		});
	});
});

function getCookie(name) {
    var cookie_name = null;
    if(document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for(var i=0; i<cookies.length; i++) {
            var cookie = $.trim(cookies[i]);
            if(cookie.substring(0, name.length + 1) === (name + '=')) {
                cookie_name = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookie_name;
}

var csrftoken = getCookie('csrftoken');
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if(!this.crossDomain) {
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    }
});
