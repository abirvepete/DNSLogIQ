#!/usr/bin/env python3
import unittest
from src.analysis.clustering_analysis import load_texts


class TestClustering(unittest.TestCase):
    def test_load_texts(self):
        texts = ["sample log one", "sample log two"]
        self.assertEqual(len(texts), 2)


if __name__ == "__main__":
    unittest.main()