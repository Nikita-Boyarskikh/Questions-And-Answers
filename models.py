# coding=utf-8
from __future__ import unicode_literals

import json
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from channels import Group

JS
=============================
==============================
  $(function () {
      var ws_path = window.location.pathname + "events/";
      console.log("Connecting to " + ws_path);
      var webSocketBridge = new channels.WebSocketBridge();
      webSocketBridge.connect(ws_path);
      webSocketBridge.listen(function (data) {
          alert("Wow! New question " + data["title"] + " by " + data["author"])
      });
============================

class Question(models.Model):
    author = models.ForeignKey(User)

    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")

    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")

    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")

    group_name = "question"

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


@receiver(post_save, sender=Question, dispatch_uid="question_websocket_event")
def question_websocket_event(sender, instance, **kwargs):
    print(Question.group_name, instance.title)
    Group(Question.group_name).send({
        'text': json.dumps({
            'title': instance.title,
            'author': instance.author.username
        })
    })
