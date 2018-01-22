import json
from channels import Group

from django.db.models import signals
from django.dispatch import receiver

from app.models import Question


@receiver(signals.post_save, sender=Question, dispatch_uid='question_websocket_event')
def question_websocket_event(_sender, instance, **_kwargs):
    Group(Question.group_name).send({
        'text': json.dumps({
            'title': instance.title,
            'author': instance.author.username
        })
    })
