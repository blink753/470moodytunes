import math
import operator
import re
from collections import defaultdict
from stemming import porter2

k = 5

def tokenize(text):
    """
    Take a string and split it into tokens on word boundaries.

    A token is defined to be one or more alphanumeric characters,
    underscores, or apostrophes.  Remove all other punctuation, whitespace, and
    empty tokens.  Do case-folding to make everything lowercase. This function
    should return a list of the tokens in the input string.
    """
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

class MoodyTunes(object):
    def  __init__(self):
        """
        """
        self.song_list = []
        self.training_set = defaultdict(list)
        self.inverted = defaultdict(list)
        self.idf = defaultdict(list)
        self.training_tf_idf = defaultdict(dict)
        self.eval_tf_idf = defaultdict(dict)
        
    def training(self, eval_list, training_set):
        """

        purpose: calculate tf-idf of the training set and eval set
        parameters:
            `eval_list`: a list of songs
            `training_set`: a dictionary matching a generic mood to its songs.
        return: None    
        """
        
        N = 0
        mag = lambda x : math.sqrt(sum(i**2 for i in x))
        tokenized_lyrics = defaultdict(list)
        
        # Creating inverted index
        for mood in training_set:
            N += len(training_set[mood])
            for song in training_set[mood]:
                s = {'mood': mood, 'artist': song['artist'], 'title': song['title']}
                self.training_set[mood].append(s)
                tokens = tokenize(song['lyrics'])
                tokenized_lyrics[song['title']] = tokens
                for token in set(tokens):
                    self.inverted[token].append(song['title'])
        
        # Calculating idf for each word and tf-idf for each song in training set
        for term in self.inverted:
            self.idf[term] = math.log(float(N)/len(self.inverted[term]),2)
            for song in tokenized_lyrics:
                count = tokenized_lyrics[song].count(term)
                if count > 0:
                    self.training_tf_idf[song][term] = self._term_tf_idf(term,count)
                    
        # Normalizing tf-idf vectors in training set
        for mood in training_set:
            for song in self.training_set[mood]:
                m = mag(self.training_tf_idf[song['title']].values())
                s = {}
                for term in self.training_tf_idf[song['title']]:
                    self.training_tf_idf[song['title']][term] = self.training_tf_idf[song['title']][term]/float(m)
                    s[term] = self.training_tf_idf[song['title']][term]
                song['tfidf'] = s

        # Calculating tf-idf for each song in eval set based on training set
        for song in eval_list:
            s = {'title': song['title'], 'artist': song['artist']}
            self.song_list.append(s)
            tokens = tokenize(song['lyrics'])
            for token in tokens:
                if token in self.idf:
                    count = tokens.count(token)
                    if count > 0:
                        self.eval_tf_idf[song['title']][token] = self._term_tf_idf(token, count)

        # Normalizing tf-idf vectors in eval set
        for song in self.song_list:
            m = mag(self.eval_tf_idf[song['title']].values())
            s = {}
            for term in self.eval_tf_idf[song['title']]:
                self.eval_tf_idf[song['title']][term] = self.eval_tf_idf[song['title']][term]/float(m)
                s[term] = self.eval_tf_idf[song['title']][term]
            song['tfidf'] = s

    def _term_tf_idf(self, token, count):
        """
        purpose: calculate tf-idf of a token.
        parameters:
            token - a term of the query
            count - the number of times the term occurs in the text (term frequency)
        returns: tf-idf of a token
        """
        if count > 0:
            return (1+math.log(count,2))*self.idf[token]
        else:
            return 0
        
    def knn(self):
        """
        purpose:  classifying a song to a generic mood based on a training set.
        parameter: None
        return: None
        """
        for song in self.song_list:
            cosine_list = []
            mood_count = defaultdict(int)
            for mood in self.training_set:
                for train_song in self.training_set[mood]:
                    cosine = sum([song['tfidf'][term]*train_song['tfidf'].get(term,0) for term in song['tfidf'].keys()])
                    cosine_list.append({'mood':train_song['mood'], 'cosine':cosine})
                neighbors = sorted(cosine_list, key=lambda k: k['cosine'])[:k]
                for cosine_song in cosine_list:
                    mood_count[cosine_song['mood']] = mood_count[cosine_song['mood']] + 1
                song_mood = max(mood_count, mood_count.get)
                song['mood'] = song_mood

if __name__=="__main__":
    knn()
