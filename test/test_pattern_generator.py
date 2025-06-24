#!/usr/bin/env python3
import unittest
from src.pattern_generator import pattern_classifier


class TestPatternGenerator(unittest.TestCase):
    def test_normalize_log_line(self):
        sample = "+0800 2025-06-22 07:45:09 INFO [4240053767 1ms] dns: cached A example.com. 123 IN A 1.2.3.4"
        norm = pattern_classifier.normalize_log_line(sample)
        self.assertNotEqual(norm, sample)


if __name__ == "__main__":
    unittest.main()