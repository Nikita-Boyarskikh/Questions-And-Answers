from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_GET
from django.utils.translation import ugettext_lazy as _

from app.utils import base_context, paginated_context, get_cur_user
from app.models import Question, Answer, Profile, Tag
from app.forms import QuestionForm, RegistrationForm

class test(generic.ListView):
    context_object_name = ''
    model = ''
    template_name = ''
    ordering = ''
    allow_empty = True
    paginator_class = ''

@require_GET
def index(request):
    questions = Question.objects.all()
    context = paginated_context(request, questions)
    context['title'] = _('Last questions')
    context['alternative_title'] = _('Hot questions')
    context['alternative_url'] = 'hot'
    return render(request, 'index.html', context)

def user(request, username):
    user = Profile.objects.get_by_name(username)
    cur_user = get_cur_user()
    if user != cur_user:
        return HttpResponseRedirect(reverse('user', cur_user.user.username))
    context = base_context(request)
    context['title'] = user.get_full_name()
    context['user'] = user
    return render(request, 'user.html', context)

@require_GET
def tag(request, tid):
    tag = get_object_or_404(Tag, id=tid)
    questions = Tag.objects.questions(tid)
    context = paginated_context(request, questions)
    context['title'] = tag.title
    context['tag'] = tag
    return render(request, 'index.html', context)

def registration(request):
    context = base_context(request)
    if request.user.is_authenticated():
        context['title'] = _('Logout')
        return render(request, 'registration/logout.html', context)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    context['title'] = _('Registration')
    context['form'] = form
    return render(request, 'registration/registration.html', context)

@require_GET
def question(request, qid):
    question = get_object_or_404(Question, id=qid)
    answers = Answer.objects.questions(qid)
    context = paginated_context(request, answers)
    context['title'] = question.title
    context['question'] = question
    context['answers'] = question.answer_set.all();
    return render(request, 'question.html', context)

def login(request):
    context = base_context(request)
    if request.user.is_autentificated():
        context['title'] = _('Logout')
        return render(request, 'logout.html', context)
    context['title'] = _('Login')
    if(request.GET):
        redirect = request.GET.get('next', '/')
        return HttpResponseRedirect(redirect)
    else:
        return render(request, 'login.html', context)

@login_required
def settings(request):
    context = base_context(request)
    context['title'] = _("User's settings")
    return render(request, 'settings.html', context)

@login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = reverse('question', question.id)
            return HttpResponseRedirect(url)
    else:
        form = QuestionForm()
    context = base_context(request)
    context['title'] = _('New question')
    context['form'] = form
    return render(request, 'ask.html', context)

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
    context['title'] = _('Answer the question') + ' ' + question.title;
    context['question'] = question;
    #url = reverse('question', question.id) + '#' + answer.id
    #return HttpResponseRedirect()
    return render(request, 'new_answer.html', context)

def answer(request, aid):
    context = base_context(request)
    answer = Answer.objects.get(id=aid)
    context['title'] = _('Answer the question') + ' ' + answer.title[:10]
    context['answer'] = answer
    return render(request, 'answer.html', context)

@require_GET
def hot(request):
    questions = Question.objects.hot()
    context = paginated_context(request, questions)
    context['title'] = _('Hot questions')
    context['alternative_title'] = _('Last questions')
    context['alternative_url'] = 'index'
    return render(request, 'index.html', context)

@require_GET
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



from django.forms import modelformset_factory

def test(request):
    AuthorFormSet = modelformset_factory(Profile, fields=('user', 'avatar'))
    if request.method == "POST":
        formset = AuthorFormSet(request.POST, request.FILES)
        if formset.is_valid():
            pass
            #formset.save()
    else:
        formset = AuthorFormSet()
    return render(request, "test.html", {
        "formset": formset,
    })
