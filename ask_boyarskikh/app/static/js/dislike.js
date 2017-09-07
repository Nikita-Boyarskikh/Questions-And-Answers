$('.dislike_js').click(function(){
	$.post('/intapi', {
	    method: 'dislike',
	    id: $(this).id
	}).done(function(data) {
	    let a = $(this).parent().find('p')[0];
            $(a).html(data);
	    console.log(data);
	}).fail(function() {
	    console.log('error');
            $(this).notify(data.error);
	});
});
