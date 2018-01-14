const likeOrDislike = (function(method) {
    return function () {
        let obj = $(this).parent().parent().parent().parent().parent().parent();
        let req = { method: method };

        switch (obj.data('class')) {
            case 'Question':
                req.qid = obj.attr('id');
                break;
            case 'Answer':
                req.aid = obj.attr('id');
                break;
            default:
                return;
        }

        $.post('/intapi', req).done(function(data) {
            let classNames = [], otherClassNames = ['has-success', 'has-error'], color = '#555';
            if (data < 0) {
                classNames = ['has-error'];
                otherClassNames = ['has-success'];
                color = '#a94442';
            } else if (data > 0) {
                classNames = ['has-success'];
                otherClassNames = ['has-error'];
                color = '#3c763d';
            }

            let a = obj.find('p.like_counter')[0];
            $(a).html(data).css('color', color);
            let parent = a.parentNode.parentNode;
            parent.classList.add(...classNames);
            parent.classList.remove(...otherClassNames);
        }).fail(function () {
            $(document).notify('Internal Server Error');
        });
    };
});

$('.like_js').click(likeOrDislike('like'));
$('.dislike_js').click(likeOrDislike('dislike'));

let $marks = $('.is_best_js');
$marks.click(function(){
	if (this.checked) {
        let req = {
            method: 'check_best_answer',
            qid: $('.question-block')[0].id,
            aid: $(this).parent().parent().parent().parent().parent().parent().parent().attr('id')
        };
        $.post('/intapi', req).done((function (data) {
            $marks.not(this).prop('checked', false);
            this.checked = true;
        }).bind(this)).fail((function () {
            this.checked = false;
        }).bind(this));
    } else {
		// prevent from extra requests
		this.checked = true;
	}
});
