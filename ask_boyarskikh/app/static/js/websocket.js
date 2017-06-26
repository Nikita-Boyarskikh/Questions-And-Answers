var socket = new WebSocket('ws://qAndAnsw.com')

socket.onopen = function(event){
	console.log('ws opened');
	var data = JSON.stringify({
		title = 'te'
	});
	socket.send(data);
};

socket.onmessage = function(event){
	console.log('receaved message: ' + resp.title);
	var resp = JSON.parse(event.data);
};

socket.onclose = function(event){
	console.log('ws closed');
};
