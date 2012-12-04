import ast
import math
import operator
import re
import utils
from collections import defaultdict
from stemming import porter2
import sys
import utils
import time
import heapq

k_neighbors = 50

def process_song(method,label):
    print 'starting %s'%label
    TRAINING_SET = utils.read_tweets(sys.argv[1])
    EVAL_SET = utils.read_tweets(sys.argv[2])
    start_time = time.time()
    method(EVAL_SET, TRAINING_SET)
    end_time = time.time()
    print 'done with %s after %.3f seconds'%(label,end_time-start_time)
    
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
        for song in training_set:
            N += 1
            #song = ast.literal_eval(song)
            s = {'mood': song['mood'], 'artist': song['artist'], 'title': song['title']}
            self.training_set[song['mood']].append(s)
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
        for mood in self.training_set:
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
            if (self.idf[token]==[]):
                return 0
            else:
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
                #neighbors = sorted(cosine_list, key=lambda k: k['cosine'])[:k_neighbors]
            neighbors = heapq.nlargest(k_neighbors, cosine_list, key=operator.itemgetter('cosine'))
            for cosine_song in neighbors:
                mood_count[cosine_song['mood']] = mood_count[cosine_song['mood']] + 1
            song_mood = max(mood_count, key=mood_count.get)
            song['mood'] = song_mood
            #print song['mood']

if __name__=="__main__":
    moodytunes = MoodyTunes()
    process_song(moodytunes.training, 'training')
##    print len(moodytunes.training_set)
##    print len(moodytunes.song_list)
    print 'starting knn'
    start_time = time.time()
    moodytunes.knn()
    end_time = time.time()
    print 'done with %s after %.3f seconds'%("knn",end_time-start_time)
##    print len(moodytunes.song_list)
##    print moodytunes.song_list[-1]
    #grabbing code here
    while True:
        print "Supported moods: Happy, Sad, Energetic, Angry, Calm"

        while True:
            mood = raw_input("What is your mood? \r\n")
            mood = mood.lower()
            if mood == "happy":
                break
            if mood == "sad":
                break
            if mood == "energetic":
                break
            if mood == "angry":
                break
            if mood == "calm":
                break
            if mood == "exit":
                sys.exit()
                
            print "Please input a valid mood: Happy, Sad, Energetic, Angry, Calm"
        query = raw_input("What other words would describe your mood? \r\n")
        #print "\nYour mood is: ",mood
        #print "Other words that describe your mood: ",query,"\r\n"
        print
        
        
        tokens = tokenize(query)
        counts = defaultdict(int)
        for token in tokens:
            counts[token]+=1
        query_tf = defaultdict(float)
        for token,count in counts.iteritems():
            query_tf[token] = moodytunes._term_tf_idf(token,count)
        
        #mag
        mag = lambda x : math.sqrt(sum(i**2 for i in x))
        
        m = mag(query_tf.values())
        #print "m"
        #print m
        for token,count in query_tf.iteritems():
            if (m != 0):
                query_tf[token] = count/m
            else:
                query_tf[token]=0
        #print query_tf
        #cosine = sum([song['tfidf'][term]*train_song['tfidf'].get(term,0) for term in song['tfidf'].keys()])
        moodlist=[]
        for song in moodytunes.song_list:
            #print max(song['mood'].iteritems(), key=operator.itemgetter(1))[0]
            #print song['mood']
            if (song['mood']==mood):
                moodlist.append(song)
        #print moodlist
        moodcosinelist = []
        for song in moodlist:
            cosine = sum([query_tf[term]*song['tfidf'].get(term,0) for term in query_tf.keys()])
            #cosine = sum([song['tfidf'][term]*query_tf[term] for term in song['tfidf'].keys()])
            moodcosinelist.append({'song':song['title'], 'cosine':cosine, 'artist': song['artist']})
        #print moodcosinelist
        neighbors = heapq.nlargest(10, moodcosinelist, key=operator.itemgetter('cosine'))
        if(neighbors==[]):
            if (moodlist !=[]):
                print moodlist[:10]
            else:
                
                print "No songs matched your mood, you are unique!\r\n"
                print moodlist[:10]
        else:
            #print neighbors
            print "Recommended Songs:"
            max_len = 0
            for song in neighbors:
                if(len("Song: "+song['song'])>max_len):
                    max_len = len("Song: "+song['song'])
            for song in neighbors:
                tabf = ""
                slen = len("Song: "+song['song'])
                while(slen<(max_len+8-(max_len%8))):
                    tabf=tabf+"\t"
                    slen = slen+8
                print "Song: "+song['song']+tabf+"Artist: "+song['artist']
                #print "Max Length: ",max_len+8-(max_len%8)," Song Length: ",slen
        print
        
