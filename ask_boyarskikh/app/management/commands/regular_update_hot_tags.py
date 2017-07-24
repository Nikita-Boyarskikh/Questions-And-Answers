#!/usr/bin/python3
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.core.cache import cache
from django.utils.translation import ugettext as _

from random import randint

from app.models import Tag, Question

class Command(BaseCommand):
	help = _('Cron script that update hot tags')
	
	def handle(self, *args, **options):
            all_tags = Question.objects.all().annotate(tag_count=Count('tags'))
            all_tags_count = 0
            for tag in all_tags:
                all_tags_count += tag.tag_count

            # Размер - отношение количества вопросов с этим тегом, умноженному на количество уникальных тегов, к количество выставленных тегов всего
            hot_tags = [{
                    'id': tag.id,
                    'size': 2 * tag.score / (all_tags_count if all_tags_count != 0 else 1) * Tag.objects.all().count(),
                    'title': tag.title,
                    'color': {
                        'r': randint(0, 255),
                        'g': randint(0, 255),
                        'b': randint(0, 255),
                    },
                } for tag in Tag.objects.all().annotate(score=Count('question'))[:20]
            ]
            cache.delete('hot_tags')
            cache.set('hot_tags', hot_tags, 31*60) # 31 минуту хранить
