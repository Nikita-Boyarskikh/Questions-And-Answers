#!/usr/bin/python3
from django.test import TestCase

class SimpleTestCase(TestCase):
    # initialisation
    def setUp(self):
        pass
    
    def test_simple(self):
        """Simple test"""
        self.assertTrue(True)
