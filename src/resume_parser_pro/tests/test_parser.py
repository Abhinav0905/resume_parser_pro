import unittest
from resume_parser.parser import ResumeParser

class TestResumeParser(unittest.TestCase):

    def setUp(self):
        self.parser = ResumeParser()

    def test_parse_valid_resume(self):
        result = self.parser.parse('path/to/valid_resume.pdf')
        self.assertIsInstance(result, dict)
        self.assertIn('name', result)
        self.assertIn('contact_info', result)

    def test_parse_invalid_resume(self):
        result = self.parser.parse('path/to/invalid_resume.pdf')
        self.assertIsNone(result)

    def test_parse_empty_file(self):
        result = self.parser.parse('path/to/empty_resume.pdf')
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()

