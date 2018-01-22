from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import login as authorize, decorators, views as auth_views

from app.utils import base_context, paginated_context, login_required_ajax
from app.models import Question, Answer, Profile, Tag
from app.forms import QuestionForm, RegistrationForm, SettingsForm, AnswerForm


def events(_request):
    return HttpResponse(status=101)


@decorators.login_required
def logout(request):
    return auth_views.logout(request, next_page='/')


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
        cur_user = request.user
    else:
        cur_user = get_object_or_404(Profile, username=uid)
    context = base_context()
    context['uid'] = uid
    context['title'] = cur_user.get_full_name()
    return render(request, 'user.html', context)


@require_GET
def tag(request, tid):
    _tag = get_object_or_404(Tag, title=tid)
    questions = Tag.objects.questions(tid)
    context = paginated_context(request, questions)
    context['title'] = _tag.title
    context['tag'] = _tag
    return render(request, 'index.html', context)


def registration(request):
    context = base_context()
    if request.user.is_authenticated:
        context['title'] = _('Logout')
        return render(request, 'registration/logout.html', context)
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            cur_user = form.save(commit=False)
            cur_user.set_password(form.cleaned_data['password'])
            cur_user.save()
            authorize(request, cur_user)
            return redirect('user')
    else:
        form = RegistrationForm()
    context['title'] = _('Registration')
    context['form'] = form
    return render(request, 'registration/registration.html', context)


def question(request, qid):
    _question = get_object_or_404(Question, id=qid)
    answers = Answer.objects.questions(qid)
    context = paginated_context(request, answers)
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/login/?next=' + request.get_full_path())
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = _question
            answer.save()
            return redirect(
                reverse('question', kwargs={'qid': _question.id}) + ('#%s' % answer.id)
            )
    else:
        form = AnswerForm()
    context['title'] = _question.title
    context['hide_text'] = False
    context['question'] = _question
    context['answers'] = _question.answer_set.all()
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
            _user = form.save(commit=False)
            cur_user = Profile.objects.get(username=request.user.username)
            if 'avatar' in form.changed_data:
                cur_user.avatar = _user.avatar
            if 'first_name' in form.changed_data:
                cur_user.first_name = _user.first_name
            if 'last_name' in form.changed_data:
                cur_user.last_name = _user.last_name
            if 'email' in form.changed_data:
                cur_user.email = _user.email
            if 'password' in form.changed_data:
                cur_user.set_password(form.cleaned_data['password'])
                cur_user.save()
                return logout(request)
            cur_user.save()
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
            _question, tags = form.save()
            if not _question.author_id:
                _question.author = request.user
            _question.save()
            for _tag in tags:
                _question.tags.add(_tag)
            return redirect('question', _question.id)
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


@require_POST
@login_required_ajax
@ensure_csrf_cookie
def intapi(request):
    if request.is_ajax():
        aid = request.POST.get('aid')
        qid = request.POST.get('qid')

        if aid:
            obj = get_object_or_404(Answer, id=aid)
        elif qid:
            obj = get_object_or_404(Question, id=qid)
        else:
            return HttpResponseBadRequest(_('Wrong data'))

        if request.POST.get('method') == 'like':
            obj.raiting += 1
            data = obj.raiting
        elif request.POST.get('method') == 'dislike':
            obj.raiting -= 1
            data = obj.raiting
        elif request.POST.get('method') == 'check_best_answer':
            answers = Answer.objects.filter(question_id=qid)
            obj = get_object_or_404(Answer, id=aid)
            if not obj.is_best:
                for i in answers.filter(is_best=True):
                    i.is_best = None
                    i.save()
                obj.is_best = True
            data = 'ok'
        else:
            data = _('Wrong method')
            return HttpResponseBadRequest(data)
        obj.save()
    else:
        data = _('Wrong request type')
        return HttpResponseBadRequest(data)
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
    content += '<h1>Hello World!</h1>'
    content += 'GET-params'
    for i in request.GET:
        content += '<br>' + str(i) + ' : ' + str(request.GET[i])
    content += '<hr>POST-params'
    for i in request.POST:
        content += '<br>' + str(i) + ' : ' + str(request.POST[i])
    content += footer
    return HttpResponse(content)
