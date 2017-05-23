$.ajax({
    url: '/',
    type: 'POST',
    data: {
        key: value,
        comment: null
    },
}).success(function(data) {
    if( data.status == 'ok' ) {
        console.log(data.comment_id);
    }
}).error(function() {
    conosle.log('error')
});
