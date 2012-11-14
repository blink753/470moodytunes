#!/usr/bin/env python
import ast
import codecs
import feedparser
import json
import os
import re
import time
import urllib
from unidecode import unidecode
from xml.dom import minidom
import xml.etree.ElementTree as ET


URLS = [
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=2/xml', 'genre': 2},
    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=6/xml', 'genre': 6},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=7/xml', 'genre': 7},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=8/xml', 'genre': 8},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=10/xml', 'genre': 10},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=11/xml', 'genre': 11},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=14/xml', 'genre': 14},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=15/xml', 'genre': 15},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=17/xml', 'genre': 17},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=18/xml', 'genre': 18},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=20/xml', 'genre': 20},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=21/xml', 'genre': 21},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=22/xml', 'genre': 22},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=23/xml', 'genre': 23},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=24/xml', 'genre': 24},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=25/xml', 'genre': 25},
##    {'url':'https://itunes.apple.com/us/rss/topsongs/limit=300/genre=50/xml', 'genre': 50},
    ]

def split(title):
    """
    purpose: splitting the song's name and artist from song's title.
    parameter:
        `title`: song's title.
    return: a list containing a song's name and artist, i.e [name, artist]
    
    """
    return re.split(' - ', title.lower())

def split_song_title(song):
    """
    """
    name = ""
    # Removing extra description
    trimmed = re.sub('\[[^]]*\]|\([^)]*\)', '', song)
    tokens = re.split(' ', trimmed)
    for token in tokens:
        if token == '':
            continue
        else:
            name = name + token + ' '

    return name[:len(name)-1]

def crawl_song(rss_feed):
    """
    purpose: crawl the top 100 songs in different genres from rss feeds.
    parameter:
        `rss_feed`: a list of rss feeds urls.
    return: None.

    """
    
    #output = open('top_songs.%d.json'%os.getpid(), 'w', 'utf-8')
##    output = codecs.open('top_songs.json', 'w', 'utf-8')
    for url in rss_feed:
        feed = feedparser.parse(url['url'])
        output = open('top_songs1.%s.json'%url['genre'], 'w')
        # checking if url is a well-formed xml
        if feed['bozo']!=1:
            for item in feed['items']:
                title_artist = split(item['title'])
                artist = title_artist[1]
                song = {'title': split_song_title(title_artist[0]), 'artist': unidecode(unicode(title_artist[1]))}
                output.write(str(json.dumps(song)) + "\n")

##        output.close()

    output.close()

def crawl_lyrics(rss_feed):
    """
    """

    for url in rss_feed:
        reader = open('top_songs1.%s.json'%url['genre'], 'r')
        output = open('lyrics1.%s.json'%url['genre'], 'w')
        fail_output = open('not_found1.%s.json'%url['genre'], 'w')
        for line in iter(reader):
            song_dict = ast.literal_eval(line)
            url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist=%s&song=%s" % (song_dict['artist'], song_dict['title'],)
            page = urllib.urlopen(url)
            if page.getcode() == 200:
                print "processing url"
                dom = minidom.parseString(page.read())
                root = ET.fromstring(dom.toprettyxml().encode('utf-8'))
                lyrics = root[-1].text
                if lyrics == None:
                    song = {'title': song_dict['title'], 'lyrics': "", 'artist': song_dict['artist']}
                    fail_output.write(str(json.dumps(song)) + "\n")
                else:
                    song = {'title': song_dict['title'], 'lyrics': lyrics, 'artist': song_dict['artist']}
                    output.write(str(json.dumps(song)) + "\n")
            else:
                print "status code not 200: ", page.getcode()
                song = {'title': song_dict['title'], 'lyrics': "", 'artist': song_dict['artist'], 'status': page.getcode()}
                fail_output.write(str(json.dumps(song)) + "\n")
                
            page.close()
            print "sleeping"
            time.sleep(60)

        output.close()
        reader.close()
        fail_output.close()
                
                

if __name__=="__main__":
    #crawl_song(URLS)
    crawl_lyrics(URLS)
    
