import os
import main
import unittest

from bs4 import BeautifulSoup
from multiprocessing import Queue
from unittest.mock import patch


class TestURLValid(unittest.TestCase):

    def test_valid_url(self):
        self.assertTrue(main.is_url_valid("https://google.com"))
        self.assertTrue(main.is_url_valid("http://www.github.com"))

    def test_invalid_url(self):
        self.assertFalse(main.is_url_valid("google.com"))
        self.assertFalse(main.is_url_valid("abcdef"))
        self.assertFalse(main.is_url_valid("https://abcdefgh"))


class TestProducerConsumer(unittest.TestCase):

    def setUp(self):
        self.mock_content = '<a href="https://www.example.com">Link</a><div></div>'
        self.input_file_name = 'test_input.txt'
        self.output_file_name = 'test_output.txt'

    def test_producer_one_link(self):
        q = Queue()
        with open(self.input_file_name, 'w') as input_file:
            input_file.write("https://www.example.com")

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = self.mock_content
            main.producer(q, self.input_file_name)

        try:
            self.assertEqual(q.qsize(), 2)
            self.assertIsNotNone(q.get())
            self.assertIsNone(q.get())
        finally:
            os.remove(self.input_file_name)

    def test_producer_two_links(self):
        q = Queue()
        with open(self.input_file_name, 'w') as input_file:
            input_file.write("https://www.example.com\nhttps://www.google.com")

        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.content = self.mock_content
            main.producer(q, self.input_file_name)

        try:
            self.assertEqual(q.qsize(), 3)
            self.assertIsNotNone(q.get())
            self.assertIsNotNone(q.get())
            self.assertIsNone(q.get())
        finally:
            os.remove(self.input_file_name)

    def test_producer_skip_wrong_link(self):
        q = Queue()
        with open(self.input_file_name, 'w') as input_file:
            input_file.write("nonsense-link\nhttps://www.example.com")

        main.producer(q, self.input_file_name)

        try:
            self.assertEqual(q.qsize(), 2)
            self.assertIsNotNone(q.get())
            self.assertIsNone(q.get())
        finally:
            os.remove(self.input_file_name)

    def test_consumer(self):
        q = Queue()

        parsed_mock_content = BeautifulSoup(self.mock_content, "html.parser")

        q.put({"markup": parsed_mock_content, "url": "https://www.example.com"})
        q.put(None)
        main.consumer(q, self.output_file_name)

        try:
            with open(self.output_file_name, 'r') as output_file:
                output_data = output_file.read()
                self.assertIn("Links at https://www.example.com\n- https://www.example.com", output_data)
        finally:
            os.remove(self.output_file_name)


if __name__ == '__main__':
    unittest.main()
