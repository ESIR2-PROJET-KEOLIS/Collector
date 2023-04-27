import unittest
from unittest.mock import MagicMock, patch
import pika
from AppCollector import verifArg, collector_choice, RequestCollector, help

class TestAppCollector(unittest.TestCase):

    def test_verifArgNotEnoughArg(self):
        with self.assertRaises(SystemExit):
            verifArg(["AppCollector.py"])

    def test_verifArgTooMuchArg(self):
        with self.assertRaises(SystemExit):
            verifArg(["AppCollector.py", "name", "REQUEST", "https://example.com", "60", "extraArg"])

    def test_verifArgCollectorType(self):
        with self.assertRaises(SystemExit):
            verifArg(["AppCollector.py", "name", "INVALID_TYPE", "https://example.com", "60"])

    def test_verifArgCollectorType2(self):
        with self.assertRaises(SystemExit):
            verifArg(["AppCollector.py", "name", "INVALID_TYPE", "https://example.com"])

    def test_verifArgTimeType(self):
        with self.assertRaises(SystemExit):
            verifArg(["AppCollector.py", "name", "REQUEST", "https://example.com", "INVALID_TIME"])

    def test_verifArgCorrect(self):
        verifArg(["AppCollector.py", "name", "REQUEST", "https://example.com", "60"])
        verifArg(["AppCollector.py", "name", "REQUEST", "https://example.com"])

    def test_help(self):
        with self.assertRaises(SystemExit):
            help()

    def test_collector_choice(self):
        self.assertIsInstance(collector_choice("REQUEST", ["REQUEST"]), RequestCollector)

    def test_collector_choice2(self):
        with self.assertRaises(NotImplementedError):
            collector_choice("CURL", ["CURL"])







if __name__ == '__main__':
    unittest.main()
