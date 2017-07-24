from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_GET, require_POST
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import hashers, login as authorize, decorators, views as auth_views

from app.utils import base_context, paginated_context, login_required_ajax, HttpResponseAjax, HttpResponseAjaxError
from app.models import Question, Answer, Profile, Tag
from app.forms import QuestionForm, RegistrationForm, SettingsForm, AnswerForm

def events(request):
    return HttpResponse(101);

@decorators.login_required
def logout(request):
    return auth_views.logout(request, next_page='/')

class BaseView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update( base_context() )
        return context

class PaginatedView(TemplateView):
    def __init__(self, objects):
        super(PaginatedView, self).__init__()
        self.objects = objects

    def get_context_data(self, **kwargs):
        context = super(BaseView, self).get_context_data(**kwargs)
        context.update( paginated_context(request, objects) )
        return context

@require_GET
def index(request):
    questions = Question.objects.all()
    context = paginated_context(request, questions)
    context['title'] = _('Last questions')
    context['alternative_title'] = _('Hot questions')
    context['alternative_url'] = 'hot'
    return render(request, 'index.html', context)

@require_GET
@decorators.login_required
def user(request, uid=None):
    if not uid:
        user = request.user
    else:
        user = get_object_or_404(Profile, username=uid)
    context = base_context()
    context['uid'] = uid
    context['title'] = user.get_full_name()
    return render(request, 'user.html', context)

@require_GET
def tag(request, tid):
    tag = get_object_or_404(Tag, title=tid)
    questions = Tag.objects.questions(tid)
    context = paginated_context(request, questions)
    context['title'] = tag.title
    context['tag'] = tag
    return render(request, 'index.html', context)

def registration(request):
    context = base_context()
    if request.user.is_authenticated():
        context['title'] = _('Logout')
        return render(request, 'registration/logout.html', context)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            authorize(request, user)
            return redirect('user')
    else:
        form = RegistrationForm()
    context['title'] = _('Registration')
    context['form'] = form
    return render(request, 'registration/registration.html', context)

def question(request, qid):
    question = get_object_or_404(Question, id=qid)
    answers = Answer.objects.questions(qid)
    context = paginated_context(request, answers)
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return redirect('/login/?next=' + request.get_full_path())
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question
            answer.save()
            return redirect(reverse('question', kwargs={'qid': question.id}) + ('#%s'%answer.id))
    else:
        form = AnswerForm()
    context['title'] = question.title
    context['hide_text'] = False
    context['question'] = question
    context['answers'] = question.answer_set.all()
    context['form'] = form
    return render(request, 'question.html', context)

def login(request):
    context = base_context()
    context['title'] = _('Login')
    template_response = auth_views.login(request)
    if hasattr(template_response, 'context_data'):
        template_response.context_data.update(context)
    return template_response

@decorators.login_required
def settings(request):
    context = base_context()
    data = {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'avatar': request.user.avatar,
        'password': '',
    }
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES)
        if form.is_valid() and form.has_changed():
            user = form.save(commit=False)
            cur_user = Profile.objects.get(username=request.user.username)
            if 'avatar' in form.changed_data:
                cur_user.avatar = user.avatar
            if 'first_name' in form.changed_data:
                cur_user.first_name = user.first_name
            if 'last_name' in form.changed_data:
                cur_user.last_name = user.last_name
            if 'email' in form.changed_data:
                cur_user.email = user.email
            if 'password' in form.changed_data:
                cur_user.set_password(form.cleaned_data['password'])
                cur_user.save()
                return logout(request)
            else:
                cur_user.save()
                return redirect('user')
        elif form.is_valid():
            return redirect('user')
    else:
        form = SettingsForm(initial=data)
    context['title'] = _("User's settings")
    context['form'] = form
    return render(request, 'settings.html', context)

@decorators.login_required
def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question, tags = form.save()
            author = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
            if not question.author_id:
                question.author = request.user._wrapped if hasattr(request.user,'_wrapped') else request.user
            question.save()
            for t in tags:
                question.tags.add(t)
            return redirect('question', question.id)
    else:
        form = QuestionForm()
    context = base_context()
    context['title'] = _('New question')
    context['form'] = form
    return render(request, 'ask.html', context)

@require_GET
def hot(request):
    questions = Question.objects.hot()
    context = paginated_context(request, questions)
    context['title'] = _('Hot questions')
    context['alternative_title'] = _('Last questions')
    context['alternative_url'] = 'index'
    return render(request, 'index.html', context)

#@require_POST
#@login_required_ajax
def intapi(request):
    if request.is_ajax():
        data = Answers.get(question_id=POST['qid'], id=POST['aid'])
    else:
        data = "Wrong"
    return HttpResponse(data)

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
