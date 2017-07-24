from channels import Group

from app.models import Question

def questions_connect(message):
    message.reply_channel.send({"accept": True})
    Group(Question.group_name).add(message.reply_channel)

def questions_disconnect(message):
    Group(Question.group_name).discard(message.reply_channel)
