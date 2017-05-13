from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.files import File

from app.models import Profile, Answer, Question, Tag

from configparser import ConfigParser
import os
import random
import datetime

class Command(BaseCommand):

	class Configuration:
		def __init__(self):
			self.config = ConfigParser()
			self.config.read("../conf/config.ini")
		
		def config_get(self, section, option, default=None):
			return self.config.get(section, option)
	
	help = 'Fill database with fake data'
	
	opts = (
		'root_path',
		'users',
		'questions',
		'answers',
		'tags',
	)
	
	def add_arguments(self, parser):
		parser.add_argument('--root-path', nargs=1, help='Path to root directiory of the project')
		parser.add_argument('--users', nargs=1, type=int, help='Number of adding users')
		parser.add_argument('--questions', type=int, nargs=1, help='Number of adding questions')
		parser.add_argument('--answers', type=int, nargs=1, help='Number of adding answers for each question')
		parser.add_argument('--tags', type=int, nargs=1, help='Number of adding tags for each answer')
	
	def handle(self, *args, **options):
		if not all([ options[opt] for opt in self.opts]):
			config = self.Configuration()
		if not options['root_path']:
			options['root_path'] = os.path.join(config.config_get('boot', 'root_dir'), config.config_get('boot', 'app'), 'app', 'uploads', 'img')
		if not options['users']:
			options['users'] = int(config.config_get('filldata', 'users'))
		if not options['questions']:
			options['questions'] = int(config.config_get('filldata', 'questions'))
		if not options['answers']:
			options['answers'] = int(config.config_get('filldata', 'answers'))
		if not options['tags']:
			options['tags'] = int(config.config_get('filldata', 'tags'))
		
		ROOT_PATH = options['root_path']
		USER_NUMBER = options['users']
		TAG_NUMBER = options['tags']
		QUESTION_NUMBER = options['questions']
		ANSWER_NUMBER = options['answers']
		
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
