import os
import random
import datetime
from configparser import ConfigParser

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.core.files import File
from django.utils.translation import ugettext as _

from app.models import Answer, Question, Tag

User = get_user_model()  # pylint: disable=invalid-name


class Command(BaseCommand):
    leave_locale_alone = True

    class Configuration:
        def __init__(self):
            self.config = ConfigParser()
            self.config.read('../conf/python/config.ini')

        def config_get(self, section, option):
            return self.config.get(section, option)

    help = _('Fill database with fake data')

    opts = (
        'root_path',
        'users',
        'questions',
        'answers',
        'tags',
    )

    def add_arguments(self, parser):
        parser.add_argument('--root-path', nargs=1, help=_('Path to root directiory of the project'))
        parser.add_argument('--users', nargs=1, type=int, help=_('Number of adding users'))
        parser.add_argument('--questions', type=int, nargs=1, help=_('Number of adding questions'))
        parser.add_argument('--answers', type=int, nargs=1, help=_('Number of adding answers for each question'))
        parser.add_argument('--tags', type=int, nargs=1, help=_('Number of adding tags for each question'))

    def _prepare_options(self, options):
        if not all([options[opt] for opt in self.opts]):
            config = self.Configuration()
            if not options['root_path']:
                options['root_path'] = os.path.join(
                    config.config_get('boot', 'root_dir'),
                    config.config_get('boot', 'app'),
                    'app', 'uploads', 'img'
                )
            if not options['users']:
                options['users'] = int(config.config_get('data', 'users'))
            if not options['questions']:
                options['questions'] = int(config.config_get('data', 'questions'))
            if not options['answers']:
                options['answers'] = int(config.config_get('data', 'answers'))
            if not options['tags']:
                options['tags'] = int(config.config_get('data', 'tags'))

        return options

    def handle(self, *args, **options):
        options = self._prepare_options(options)
        users = _fill_users(options['users'], options['root_path'])
        tags = _fill_tags(options['tags'])
        questions = _fill_questions(options['questions'], users=users, tags=tags)
        _fill_answers(options['answers'], users=users, questions=questions)


def _fill_users(users_number, root_path):
    users = []

    for i in range(users_number):
        user = User.objects.create_user(
            username=_('User') + str(i),
            password='pass' + str(i),
            email='user' + str(i) + '@ask.ru',
            first_name='lol',
            last_name='kek',
        )
        tmp_f = open(os.path.join(root_path, 'user' + str(i) + '.png'), 'rb')
        f = File(tmp_f)
        user.avatar.save('User' + str(i) + '.png', f, save=True)
        users.append(user)

    return users


def _fill_answers(answers_number, users, questions):
    answers = []

    for i in range(answers_number):
        answer = Answer()
        answer.text = _('A lot of text...\n')
        answer.raiting = random.randint(0, 10)
        answer.question = questions[random.randint(0, len(questions) - 1)]
        answer.author = users[random.randint(0, len(users) - 1)]
        answer.save()
        answers.append(answer)

    return answers


def _fill_questions(questions_number, users, tags):
    questions = []

    for i in range(questions_number):
        question = Question()
        question.title = _('question') + str(i)
        question.author = users[random.randint(0, len(users) - 1)]
        question.text = _('A lot of text...\n')
        question.raiting = random.randint(-10, 10)
        question.is_published = True
        question.create_date = datetime.date.today()
        question.save()

        tag_number = random.randint(0, min(len(tags), 3))

        for n in range(tag_number):
            tag_idx = random.randint(0, len(tags))
            if tag_idx != len(tags):
                question.tags.add(tags[tag_idx])
        questions.append(question)

    return questions


def _fill_tags(tags_number):
    tags = []

    for i in range(tags_number):
        tag = Tag()
        tag.count = 0
        tag.title = 'tag' + str(i)
        tag.save()
        tags.append(tag)

    return tags
