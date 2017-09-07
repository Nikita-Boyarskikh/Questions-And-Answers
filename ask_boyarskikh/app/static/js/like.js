$('.like_js').click(function(){
    $.post('/intapi', {
        method: 'like',
        id: $(this).id
    }).done(function(data) {
        var a = $(this).parent().find('p')[0];
        $(a).html(data);
        console.log(data);
    }).fail(function() {
        console.log('error');
        $(this).notify(data.error)
    });
});
