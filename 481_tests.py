import unittest
from unittest.mock import patch
import logging
from logging.handlers import RotatingFileHandler
import _get_handler

class TestGetHandler(unittest.TestCase):

    @patch('logging.FileHandler', autospec=True)
    @patch('logging.StreamHandler', autospec=True)
    @patch('logging.NullHandler', autospec=True)
    def test_get_handler_file(self, mock_null_handler, mock_stream_handler, mock_file_handler):
        settings = {
            "LOG_FILE": "test.log",
            "LOG_FILE_APPEND": False,
            "LOG_ROTATING": False,
            "LOG_ENABLED": True,
            "LOG_ENCODING": "utf-8"
        }
        handler = _get_handler(settings)
        mock_file_handler.assert_called_once_with("test.log", mode="w", encoding="utf-8")
        self.assertIsInstance(handler, logging.FileHandler)

    @patch('logging.FileHandler', autospec=True)
    @patch('logging.StreamHandler', autospec=True)
    @patch('logging.NullHandler', autospec=True)
    def test_get_handler_rotating_default(self, mock_null_handler, mock_stream_handler, mock_file_handler):
        settings = {
            "LOG_FILE": "test.log",
            "LOG_ROTATING": True,
            "LOG_ENABLED": True,
            "LOG_ENCODING": "utf-8"
        }
        handler = _get_handler(settings)
        mock_file_handler.assert_called_once_with("test.log", mode="a", encoding="utf-8")
        self.assertIsInstance(handler, RotatingFileHandler)

    @patch('logging.FileHandler', autospec=True)
    @patch('logging.StreamHandler', autospec=True)
    @patch('logging.NullHandler', autospec=True)
    def test_get_handler_rotating_custom(self, mock_null_handler, mock_stream_handler, mock_file_handler):
        settings = {
            "LOG_FILE": "test.log",
            "LOG_ROTATING": True,
            "LOG_MAX_BYTES": 1024,
            "LOG_BACKUP_COUNT": 5,
            "LOG_ENABLED": True,
            "LOG_ENCODING": "utf-8"
        }
        handler = _get_handler(settings)
        mock_file_handler.assert_called_once_with("test.log", mode="a", encoding="utf-8")
        self.assertIsInstance(handler, RotatingFileHandler)
        self.assertEqual(handler.maxBytes, 1024)
        self.assertEqual(handler.backupCount, 5)

    @patch('logging.FileHandler', autospec=True)
    @patch('logging.StreamHandler', autospec=True)
    @patch('logging.NullHandler', autospec=True)
    def test_get_handler_rotating_no_file(self, mock_null_handler, mock_stream_handler, mock_file_handler):
        settings = {
            "LOG_FILE": "",
            "LOG_ROTATING": True,
            "LOG_ENABLED": True,
            "LOG_ENCODING": "utf-8"
        }
        handler = _get_handler(settings)
        mock_null_handler.assert_called_once_with()
        self.assertIsInstance(handler, logging.NullHandler)

if __name__ == '__main__':
    unittest.main()