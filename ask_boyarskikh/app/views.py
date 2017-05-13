from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from app.utils import base_context, paginated_context
from app.models import Question, Answer, Profile, Tag, User

def index(request):
    questions = Question.objects.all()
    context = paginated_context(request, questions)
    context['title'] = 'Last questions'
    context['alternative_title'] = 'Hot questions'
    context['alternative_url'] = 'hot'
    return render_to_response('index.html', context)

def user(request, username):
    user = User.objects.get(username=username)
    context = base_context(request)
    context['title'] = user.get_full_name()
    context['user'] = user
    return render_to_response('user.html', context)

def tag(request, tid):
    tag = get_object_or_404(Tag, tid=tid)
    questions = Questions.objects.tag(tid)
    context = paginated_context(request, questions)
    context['title'] = tag.title
    content['tag'] = tag
    return render_to_response('tag.html', context)

def registration(request):
    context = base_context(request)
    context['title'] = 'Registration'
    return render_to_response('registration.html', context)

def question(request, qid):
    question = get_object_or_404(Question, Question_id=qid)
    answers = Answer.objects.questions(qid)
    context = paginated_context(request, answers)
    context['title'] = question.title
    context['question'] = question
    return render_to_response('question.html', context)

def login(request):
    context = base_context(request)
    context['title'] = 'Login'
    if(request.GET.has('request')):
        redirect = request.GET.get('redirect', '/')
        return HttpResponseRedirect(redirect)
    else:
        return render_to_response('login.html', context)

@login_required
def settings(request):
    context = base_context(request)
    context['title'] = "User's settings"
    return render_to_response('settings.html', context)

@login_required
def ask(request):
    context = base_context(request)
    context['title'] = 'New question'
    return render_to_response('ask.html', context)

@login_required
def new_answer(request):
    try:
        qid = int(request.GET.get('question'));
    except ValueError:
        qid = None
    
    if qid:
        question = Question.objects.get(id=qid);
    else:
        question = None
    
    context = base_context(request)
    context['title'] = 'Answer the question ' + question.title;
    context['question'] = question;
    
    return render_to_response('new_answer.html', context)

def answer(request, aid):
    context = base_context(request)
    answer = Answer.objects.get(id=aid)
    context['title'] = 'Answer the question ' + answer.title[:10]
    context['answer'] = answer
    return render_to_response('answer.html', context)

def hot(request):
    questions = Question.objects.hot()
    context = paginated_context(request, questions)
    context['title'] = 'Hot questions'
    context['alternative_title'] = 'Last questions'
    context['alternative_url'] = 'index'
    return render_to_response('index.html', context)

def hello(request):
    header = '''
<html>
    <head>
        <title>Hello!</title>
    </head>
    <body>
'''
    footer = '''
    </body>
</html>
'''
    content = header
    content = '<h1>Hello World!</h1>'
    content = content + 'GET-params'
    for i in request.GET:
        content += '<br>' + str(i) + ' : ' + str(request.GET[i])
    content += '<hr>POST-params'
    for i in request.POST:
        content += '<br>' + str(i) + ' : ' + str(request.POST[i])
    content += footer
    return HttpResponse(content)
