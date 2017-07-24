$(document).ready(function(){
	// websockets
	var ws_path = 'ws://' + window.location.host + "/events";
	console.log("Connecting to " + ws_path);
	var webSocketBridge = new channels.WebSocketBridge();
	webSocketBridge.connect(ws_path);
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

	// fade out all .alert-danger
	list = $(".alert-danger");
	var i = -1;
	function hide_errors(){
		if(i == list.length) return;
		i++;
		$(list[i]).fadeOut(2000, hide_errors);
	};
	hide_errors();
});
