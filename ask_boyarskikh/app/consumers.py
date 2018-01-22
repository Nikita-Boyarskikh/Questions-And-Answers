from channels import Group

from app.models import Question


def ws_connect(message):
    Group(Question.group_name).add(message.reply_channel)


def ws_disconnect(message):
    Group(Question.group_name).discard(message.reply_channel)
