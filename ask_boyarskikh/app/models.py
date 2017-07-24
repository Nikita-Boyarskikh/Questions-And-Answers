import random

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Count
from django.utils.translation import string_concat, ugettext_lazy as _
from django.core.mail import send_mail

class Like(models.Model):
    user = models.ForeignKey('Profile', verbose_name=_('User'))
    question = models.ForeignKey('Question', verbose_name=_('Question'))
    answer = models.ForeignKey('Answer', verbose_name=_('Answer'))

    def __str__(self):
        return 'user "%s" likes "%s" answer' % (self.user, self.answer)

    class Meta:
        verbose_name = _('Like')
        verbose_name_plural = _('Likes')

class QuestionManager(models.Manager):
    def answers_count(self):
        return Question.answers_set.group_by('question_id').annotate(Count('question_id'))
    def published(self):
        return self.filter(is_published=True)
    def hot(self):
        return self.order_by('-raiting')

class Question(models.Model):
    title = models.CharField(max_length=30, verbose_name=_('Title'), db_index = True)
    text = models.TextField(verbose_name=_('Text'))
    raiting = models.SmallIntegerField(default=0, editable=False, verbose_name=_('Raiting'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create time'))

    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('Tag'))
    author = models.ForeignKey('Profile', verbose_name=_('Author'))

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date', 'title']
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

class ProfileManager(UserManager):
    pass

class Profile(AbstractUser):
    def _get_image_name(self, image_name):
        return str(self.id) + image_name.split('.')[-1]

    def get_full_name(self):
        try:
            full_name = self.first_name.capitalize() + ' ' + self.last_name.capitalize()
        except TypeError:
            full_name = ' '
        if full_name == ' ':
            full_name = self.username
        return full_name

    avatar = models.ImageField(
        _('Avatar'),
        upload_to=_get_image_name,
        max_length=1024,
    )

    objects = ProfileManager()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class TagManager(models.Manager):
    def questions(self, tid):
        return self.get(title=tid).question_set.all()[:20]

class Tag(models.Model):
    title = models.SlugField(max_length=255, verbose_name=_('Title'), unique=True, db_index=True)

    objects = TagManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

class AnswerManager(models.Manager):
    def questions(self, qid):
        return Answer.objects.filter(question_id=qid)

class Answer(models.Model):
    text = models.TextField(verbose_name=_('Text'))
    raiting = models.SmallIntegerField(default=0, verbose_name=_('Raiting'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create time'))
    is_best = models.NullBooleanField(verbose_name=_('Is best'))

    question = models.ForeignKey('Question', verbose_name=_('Question'), db_index = True)
    author = models.ForeignKey('Profile', verbose_name=_('Author'))

    objects = AnswerManager()

    def save(self, *args, **kwargs):
        super(Answer, self).save(*args, **kwargs)
        author = self.question.author
        if author.email:
            send_mail('New answer to your question!',
            _('Hi, dear %s!') % author.get_full_name(),
                'noreply@qAndAnsw.com',
                [author.email], fail_silently=True, html_message='<p>' + str(
                _('You received a new answer to your question is "{}"!').format(
                    '<a href="%s">%s</a>' % ('qAndAnsw.com' + reverse('question', kwargs={'qid': self.question_id}), self.question.title)
                )) + '</p><p>' + str(
                _('To see what you said, click on this link: {}').format(
                    '<a href="%s#%d">%s#%d</a>' % (('qAndAnsw.com' + reverse('question', kwargs={'qid': self.question_id}), self.id) * 2)
                )) + '<br / ><p>' + str(
                _('Best regards, site administration {}').format(
                    '<a href="%s">%s</a></p>' % (('qAndAnsw.com',) * 2)
                ))
            )

    def __str__(self):
        return self.text[:30] + '...'

    class Meta:
        ordering = ['-raiting', 'create_date']
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
        unique_together = [
            ('question', 'is_best'),
        ]
