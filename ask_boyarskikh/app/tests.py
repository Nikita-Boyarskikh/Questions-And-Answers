from django.test import TestCase

class SomeTestCase(TestCase):
    # initialisation
    def setUp(self):
        pass

    # 1st test function
    def test_some_test(self):
        self.assertEqual(1, 1)
        self.assertTrue(True)
