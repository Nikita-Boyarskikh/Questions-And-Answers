$('.dislike_js').click(function(){
	let obj = $(this).parent().parent().parent().parent().parent().parent();
    let req = {
	    method: 'dislike',
        id: obj.attr('id'),
        class: obj.data('class')
	};
    console.log(req);
	$.post('/intapi', req).done(function(data) {
	    let a = $(this).parent().find('p')[0];
        $(a).html(data);
	    console.log(data);
	}).fail(function() {
	    console.log('error');
        $(this).notify('Internal Server Error');
	});
});
