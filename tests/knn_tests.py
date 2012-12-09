#!/usr/bin/env python
# script to test the knn algorithm

import unittest
import knn

TRAINING_SET = [
    {"artist":"Beach Boys", "title": "Good Vibrations", "lyrics":"good vibrations (Good vibrations, oom)", "mood": "happy"},
    {"artist":"Aly & AJ", "title": "Walking On Sunshine", "lyrics":"good walking sunshine walking sunshine", "mood": "happy"},
    {"artist":"The Beatles", "title":"Yesterday", "lyrics":"long for yesterday Yesterday", "mood":"sad"},
    {"artist":"Billie Holiday", "title":"Gloomy Sunday", "lyrics":"yesterday Gloomy Sunday yesterday", "mood":"sad"},
    ]

EVAL_SET = [
    {"artist":"Anh Pham", "title":"Good Song", "lyrics":"good long"},
    {"artist":"Zach Pollack", "title":"Sad Song", "lyrics":"yesterday oom crazy"},
    ]

class TestKNN(unittest.TestCase):
    def setUp(self):
        self.MoodyTunes = knn.MoodyTunes()
        self.MoodyTunes.training(iter(EVAL_SET), iter(TRAINING_SET))
        self.MoodyTunes.knn()

    def test_tf_idfs(self):
        test_dict = {}
        good_vibrat_tfidf = {"good":0.4082, "vibrat":0.8165, "oom":0.4082}
        test_dict = self.MoodyTunes.training_set["happy"][0]["tfidf"]
        self.assertTrue(test_dict.viewkeys(), good_vibrat_tfidf.viewkeys())
        for term,tf_idf in good_vibrat_tfidf.iteritems():
            self.assertAlmostEqual(tf_idf, test_dict[term],4)
        
        walk_sun_tfidf = {"good":0.1741, "sunshin": 0.6963, "walk":0.6963}
        test_dict = self.MoodyTunes.training_set["happy"][1]["tfidf"]
        self.assertTrue(test_dict.viewkeys(), walk_sun_tfidf.viewkeys())
        for term,tf_idf in walk_sun_tfidf.iteritems():
            self.assertAlmostEqual(tf_idf, test_dict[term],4)
            
        yesterday_tfidf = {"yesterday":0.5774, "for":0.5774, "long":0.5774}
        test_dict = self.MoodyTunes.training_set["sad"][0]["tfidf"]
        self.assertTrue(test_dict.viewkeys(), yesterday_tfidf.viewkeys())
        for term,tf_idf in yesterday_tfidf.iteritems():
            self.assertAlmostEqual(tf_idf, test_dict[term],4)
            
        gloomy_sunday_tfidf = {"yesterday":0.5774, "sunday":0.5774, "gloomi":0.5774}
        test_dict = self.MoodyTunes.training_set["sad"][1]["tfidf"]
        self.assertTrue(test_dict.viewkeys(), gloomy_sunday_tfidf.viewkeys())
        for term,tf_idf in gloomy_sunday_tfidf.iteritems():
            self.assertAlmostEqual(tf_idf, test_dict[term],4)
        
        eval_1_tfidf = {"good":0.4472, "long":0.8944}
        test_dict = self.MoodyTunes.song_list[0]["tfidf"]
        self.assertTrue(test_dict.viewkeys(), eval_1_tfidf.viewkeys())
        for term,tf_idf in eval_1_tfidf.iteritems():
            self.assertAlmostEqual(tf_idf, test_dict[term],4)
            
        eval_2_tfidf = {"yesterday":0.4472, "oom":0.8944}
        test_dict = self.MoodyTunes.song_list[1]["tfidf"]
        self.assertTrue(test_dict.viewkeys(), eval_2_tfidf.viewkeys())
        for term,tf_idf in eval_2_tfidf.iteritems():
            self.assertAlmostEqual(tf_idf, test_dict[term],4)
            
    def test_knn(self):
        self.assertTrue(self.MoodyTunes.song_list[0]["mood"], "happy")
        self.assertTrue(self.MoodyTunes.song_list[1]["mood"], "sad")
            
         

if __name__ == '__main__':
    unittest.main()
