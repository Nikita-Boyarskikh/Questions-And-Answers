#!/usr/bin/python3
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.core.cache import cache
from django.utils.translation import ugettext as _

from app.models import Question, Answer, Profile

class Command(BaseCommand):
	help = _('Cron script that update best users')
	
	def handle(self, *args, **options):
            all_questions = Question.objects.all().count()
            bestusers = [{
                    'avatar': user.avatar,
                    'username': user.username,
                    'get_full_name': user.get_full_name(),
                } for user in Profile.objects.all().annotate(score=(Count('question') + Count('answer')))[:10]
            ]
            cache.delete('bestusers')
            cache.set('bestusers', bestusers, 31*60) # 31 минуту хранить
