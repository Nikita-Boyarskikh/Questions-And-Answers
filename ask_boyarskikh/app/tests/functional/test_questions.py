from app.tests.functional.test_helper import ApplicationLiveServerTestCase
from app.models import Question


class QuestionsLiveTest(ApplicationLiveServerTestCase):
    fixtures = ['tags.yaml', 'profiles.yaml', 'questions.yaml']

    def test_all_questions_displayed(self):
        self.driver.get(self.live_server_url)
        self.assertEquals(len(self.driver.find_elements_by_class_name('question-block')), Question.objects.count())

    def test_main_page_title(self):
        self.driver.get(self.live_server_url)
        self.assertIn('AskIt!', self.driver.title)
