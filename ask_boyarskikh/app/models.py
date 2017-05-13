from __future__ import unicode_literals
import random
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

class QuestionManager(models.Manager):
    def answers_count(self):
        return Question.answers_set.group_by('question_id').annotate(Count('question_id'))
    def published(self):
        return self.filter(is_published=True)
    def hot(self):
        return self.order_by('-raiting')

class Question(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Заголовок", db_index = True)
    text = models.TextField(verbose_name=u"Текст")
    raiting = models.SmallIntegerField(default=0, verbose_name=u"Рейтинг")
    is_published = models.BooleanField(verbose_name=u"Опубликована")
    create_date = models.DateField(verbose_name=u"Время создания")

    tags = models.ManyToManyField('Tag', blank=True, verbose_name=u"Тег")
    author = models.ForeignKey('Profile', verbose_name=u"Автор")

    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['create_date']
        verbose_name = u"Вопрос"
        verbose_name_plural = u"Вопросы"

class Profile(models.Model):
    def _get_image_name(self, image_name):
        return str(self.user.id) + image_name.split('.')[-1]

    raiting = models.SmallIntegerField(default=0, verbose_name=u"Рейтинг")
    avatar = models.ImageField(upload_to=_get_image_name, max_length=1024, verbose_name=u"Аватар")

    user = models.OneToOneField(User, verbose_name=u"Джанго-пользователь")

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['user__username']
        verbose_name = u"Пользователя"
        verbose_name_plural = u"Пользователи"

class BestProfileManager(models.Manager):
    def get(self):
        return self.all()[:5]

class BestProfile(models.Model):
    profile = models.OneToOneField(Profile)
    objects = BestProfileManager()

    class Meta:
        ordering = ['-profile__raiting']
        verbose_name = u"Лучший пользователь"
        verbose_name_plural = u"Лучшие пользователи"

class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name=u"Название", db_index = True)
    count = models.PositiveIntegerField(verbose_name=u"Количество постов с этим тегом")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['count']
        verbose_name = u"Тег"
        verbose_name_plural = u"Теги"

class HotTagsManager(models.Manager):
    def get(self):
        return self.all()[:5]

class HotTags(models.Model):
    tag = models.OneToOneField(Tag)
    objects = HotTagsManager()

    def size(self):
        return random.random()*3 + 0.5

    def title(self):
        return self.tag.title

    def color(self):
        return {
                   'r': random.random()*200,
                   'g': random.random()*200,
                   'b': random.random()*200,
               }

    def __str__(self):
        return str(self.tag)

    class Meta:
        verbose_name = u"Горячий тег"
        verbose_name_plural = u"Горячие теги"

class AnswerManager(models.Manager):
    def questions(self, qid):
        return Answer.objects.filter(Question_id=qid)

class Answer(models.Model):
    text = models.TextField(verbose_name=u"Текст")
    raiting = models.SmallIntegerField(default=0, verbose_name=u"Рейтинг")

    question = models.ForeignKey('Question', verbose_name=u"Вопрос", db_index = True)
    author = models.ForeignKey('Profile', verbose_name=u"Автор")

    objects = AnswerManager()

    def __str__(self):
        return self.text[:30] + '...'

    class Meta:
        verbose_name = u"Ответ"
        verbose_name_plural = u"Ответы"
