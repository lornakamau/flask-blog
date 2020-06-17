import unittest
from app.models import Quote

class QuoteModelTest(unittest.TestCase):
    def setUp(self):
        self.new_quote= Quote(author="lorna", id=1, quote="I am great")

    def test_instance(self):
         self.assertTrue(isinstance(self.new_quote, Quote))

    def test_initialization(self):
        self.assertEqual(self.new_quote.author, 'lorna' )
        self.assertEqual(self.new_quote.quote, 'I am great' )