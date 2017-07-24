let $marks = $('.is_best_js');
$marks.change(function(){
	$marks.not(this).prop('checked', false);
	$.post('/intapi', {
		method: 'check_best_answer',
		qid: $('.question-block')[0].id,
		aid: $(this).parent().parent().parent().parent().parent().parent().id
	}).done(function(data){
		console.log(data);
	}).fail(function(){
		console.log('error');
	});
});
