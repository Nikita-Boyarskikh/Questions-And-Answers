from __future__ import unicode_literals
import random

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# NOTE: F() help save consistents of data in DB. If you're use field from DB in some expression, you're should use F() object like this:
# NOT field += 1 BUT field = F('field') + 1
from django.db.models import Count, F
from django.utils.translation import string_concat, ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    title = models.CharField(max_length=255, verbose_name=_('Title'), db_index = True)
    text = models.TextField(verbose_name=_('Text'))
    raiting = models.SmallIntegerField(default=0, editable=False, verbose_name=_('Raiting'))
    is_published = models.BooleanField(default=True, editable=False, verbose_name=_('Published'))
    create_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Create time'))

    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('Tag'))
    author = models.ForeignKey('Profile', verbose_name=_('Author'))
#    right_answer = models.ForeignKey('Answer', blank=True, verbose_name=_('Right answer'))

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['create_date', 'title']
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')

class ProfileManager(UserManager):
    def get_by_name(self, username):
        return self.get(username=username)

class Profile(AbstractUser):
    def _get_image_name(self, image_name):
        return str(self.user.id) + image_name.split('.')[-1]
    
    avatar = models.ImageField(
        _('Avatar'),
        upload_to=_get_image_name,
        max_length=1024,
    )

#    objects = ProfileManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class TagManager(models.Manager):
    def questions(self, tid):
        return self.get(id=tid).question_set.order_by('-raiting').all()[:20]

class Tag(models.Model):
    title = models.SlugField(max_length=255, verbose_name=_('Title'))

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

    question = models.ForeignKey('Question', verbose_name=_('Question'), db_index = True)
    author = models.ForeignKey('Profile', verbose_name=_('Author'))

    objects = AnswerManager()

    def save(self, *args, **kwargs):
        super(Answer, self).save(*args, **kwargs)
        #TODO send e-mail

    def __str__(self):
        return string_concat(self.text[:30] + _('...'))

    class Meta:
        ordering = ['-raiting', 'create_date']
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')
