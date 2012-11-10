#!/usr/bin/env python
import feedparser
import json
import re
import os

URLS = ['https://itunes.apple.com/us/rss/topsongs/limit=100/genre=20/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=2/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=22/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=5/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=6/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=17/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=50/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=18/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=8/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=11/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=12/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=14/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=15/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=24/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=21/xml',
        'https://itunes.apple.com/us/rss/topsongs/limit=100/genre=10/xml',
        ]

def split(title):
    """
    purpose: splitting the song's name and artist from song's title.
    parameter:
        `title`: song's title.
    return: a list containing a song's name and artist, i.e [name, artist]
    
    """
    return re.split(' - ', title.lower())

def crawl(rss_feed):
    """
    purpose: crawl the top 100 songs in different genres from rss feeds.
    parameter:
        `rss_feed`: a list of rss feeds urls.
    return: None.

    """
    
    output = open('top_songs.json', 'w')
    for url in rss_feed:
        feed = feedparser.parse(url)
        # checking if url is a well-formed xml
        if feed['bozo']!=1:
            for item in feed['items']:
                title_artist = split(item['title'])
                song = {'title': title_artist[0], 'artist': title_artist[1]}
                output.write(str(json.dumps(song)) + "\n")

    output.close()

if __name__=="__main__":
    crawl(URLS)
