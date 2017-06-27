$('#like').click(function(){
	$.ajax({
	    url: '/intapi',
	    type: 'POST',
	    data: {
	        method: 'like',
	        elem: $(this).id
	    },
	}).success(function(data) {
	    if( data.status == 'ok' ) {
	        $(this).value++;
	        console.log('ok');
	    }
	}).error(function() {
	    conosle.log('error');
	});
});
