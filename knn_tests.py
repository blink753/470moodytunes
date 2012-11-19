#!/usr/bin/env python
# script to test the knn algorithm

import unittest

TRAINING_SET = {
    "happy": [
        {"artist":"Beach Boys", "song" = "Good Vibrations", "lyrics":"good vibrations (Good vibrations, oom)"},
        {"artist":"Aly & AJ", "song" = "Walking On Sunshine", "lyrics":"good walking sunshine walking sunshine"},
    ],
    "sad": [
        {"artist":"The Beatles", "song":"Yesterday", "lyrics":"long for yesterday Yesterday"},
        {"artist":"Billie Holiday", "song":"Gloomy Sunday", "lyrics":"yesterday Gloomy Sunday yesterday"}
    ]
}

EVAL_SET = [
    {"artist":"Anh Pham", "song":"Good Song", "lyrics":"good long"},
    {"artist":"Zach Pollack", "song":"Sad Song", "lyrics":"yesterday oom crazy"},
]

class TestKNN(unittest.TestCase):
    def setUp(self):
        self.ranker = pagerank.PageRanker()
        self.ranker.calc_pagerank(MENTION_CORPUS)

    # Tests to check calculations for PageRank
    def test_power_of_zero(self):
        # calculate PR = x * (P^0)
        calculated_result = np.matrix([[0.25, 0.25, 0.25, 0.25]])
        actual_result = self.ranker.calc_prob_vector(0)
        self.assertTrue(np.allclose(actual_result, calculated_result))
         

if __name__ == '__main__':
    unittest.main()
