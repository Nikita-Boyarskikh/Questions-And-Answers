from app.models import Profile, Answer, Question, Tag
from django.contrib.auth.models import User
from django.core.files import File
from configparser import ConfigParser
import os
import random
import datetime

class Configuration:
	def config_get(self, section, option, default=None):
		self.config = ConfigParser()
		self.config.read("../conf/config.ini")
		return self.config.get(section, option)

config = Configuration()

ROOT_PATH = os.path.join(config.config_get('boot', 'root_dir'), config.config_get('boot', 'app'), 'app', 'uploads', 'img')
USER_NUMBER = int(config.config_get('filldata', 'users'))
QUESTION_NUMBER = int(config.config_get('filldata', 'questions'))
ANSWER_NUMBER = int(config.config_get('filldata', 'answers'))
TAG_NUMBER = int(config.config_get('filldata', 'tags'))

users = []
tags = []
questions = []

for i in range(USER_NUMBER):
    user = User.objects.create_user(
        'User' + str(i),
        password = 'pass' + str(i),
        email = 'user' + str(i) + '@ask.ru'
    )
    profile = Profile()
    profile.user = user
    profile.raiting = 0
    tmp_f = open(os.path.join(ROOT_PATH, 'user' + str(i) + '.png'), 'rb')
    f = File(tmp_f)
    profile.avatar.save('User' + str(i) + '.png', f, save=True)
    users.append(profile)

for i in range(TAG_NUMBER):
    tag = Tag()
    tag.count = 0
    tag.title = 'tag' + str(i)
    tag.save()
    tags.append(tag)

for i in range(QUESTION_NUMBER):
    question = Question()
    question.title = 'question' + str(i)
    question.author = users[random.randint(0, len(users) - 1)]
    question.text = '\n'.join([ 'Много-много текста' for _ in range(10) ])
    question.raiting = random.randint(-10, 10)
    question.is_published = True
    question.create_date = datetime.date.today()
    question.save()
    for n in range(0, len(tags)):
        t = random.randint(0, TAG_NUMBER)
        if t != TAG_NUMBER:
            question.tags.add(tags[t])
    questions.append(question)

for i in range(ANSWER_NUMBER):
    answer = Answer()
    answer.text = '\n'.join([ 'Много-много текста' for _ in range(10) ])
    answer.raiting = random.randint(0, 10)
    answer.question = questions[random.randint(0, len(questions) - 1)]
    answer.author = users[random.randint(0, len(users) - 1)]
    answer.save()
