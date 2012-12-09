#!/usr/bin/env python
# web server for tweet search
# You should not need to edit this file.

import time

import bottle
import knn
import utils
#from settings import settings

_searcher = None

@bottle.route('/search')
def search(name='World'):
    global _searcher
    query = bottle.request.query.q
    
    mood = bottle.request.environ.get('mood_dropbox')
    que = bottle.request.environ.get('query')
    print "MOOD!!!!!!"
    print mood
    print "QUERY!!!"
    print que
    
    start_time = time.time()
    tweets = _searcher.search_results('happy', query)
    end_time = time.time()

    return dict(
            tweets = tweets,
            #author = settings['author'],
            #agree_to_honor_code = settings['agree_to_honor_code'],
            count = len(tweets),
            time = end_time - start_time,
            )


@bottle.route('/')
def index():
    return bottle.static_file('index.html', root='static')


@bottle.route('/favicon.ico')
def favicon():
    return bottle.static_file('favicon.ico', root='static')


@bottle.route('/static/<filename:path>')
def server_static(filename):
    return bottle.static_file(filename, root='static')


if __name__=="__main__":
    #_searcher = tweetsearch.TweetSearch()
    #tweets = utils.read_tweets()
    #_searcher.index_tweets(tweets)
    _searcher = knn.MoodyTunes()
    knn.process_song(_searcher.training, 'training')
    _searcher.knn()
    bottle.run(host='localhost',
               port=8080,
               reloader=True)
