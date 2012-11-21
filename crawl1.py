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

    output.close()

def crawl_lyrics():
    """
    """

    reader = open('not_found.json', 'r')
    output = open('new_lyrics.json', 'a')
    fail_output = open('leftover.json', 'a')
    for line in iter(reader):
        song_dict = ast.literal_eval(line)
        url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist=%s&song=%s" % (song_dict['artist'], song_dict['title'],)
        page = urllib.urlopen(url)
        if page.getcode() == 200:
            #print "processing url"
            dom = minidom.parseString(page.read())
            root = ET.fromstring(dom.toprettyxml().encode('utf-8'))
            page.close()
            time.sleep(60)
            count = 0
            lyric_found = False
            for child in root[:len(root)-1]:
                if child[5].text.lower() == song_dict['artist'] and song_dict['title'] in child[6].text.lower()\
                   and "app/add" not in child[3].text:
                    lyricID = child[2].text
                    checksum = child[1].text
                    lyric_url = "http://api.chartlyrics.com/apiv1.asmx/GetLyric?lyricId=%s&lyricCheckSum=%s" %(lyricID, checksum,)
                    page = urllib.urlopen(lyric_url)
                    print child[5].text, "=", child[6].text
                    if page.getcode() == 200:
                        dom = minidom.parseString(page.read())
                        root = ET.fromstring(dom.toprettyxml().encode('utf-8'))
                        page.close()
                        lyrics = root[-1].text
                        #print "found lyric", lyricID, checksum
                        song = {'title': song_dict['title'], 'lyrics': lyrics, 'artist': song_dict['artist']}
                        output.write(str(json.dumps(song)) + "\n")
                        lyric_found = True
                        break

                    else:
                        count+=1
                        print "status code not 200: ", page.getcode()
                        song = {'title': song_dict['title'], 'lyrics': "", 'artist': song_dict['artist']}
                        fail_output.write(str(json.dumps(song)) + "\n")
                else:
                    count+=1
                    lyric_found = False
                        
            else:
                if count == len(root[:len(root)-1]) and lyric_found == False:
                    song = {'title': song_dict['title'], 'lyrics': "", 'artist': song_dict['artist']}
                    fail_output.write(str(json.dumps(song)) + "\n")
                    
        else:
            print "status code not 200: ", page.getcode()
            song = {'title': song_dict['title'], 'lyrics': "", 'artist': song_dict['artist'], 'status': page.getcode()}
            fail_output.write(str(json.dumps(song)) + "\n")
            
        #print "sleeping"
        time.sleep(60)

    output.close()
    reader.close()
    fail_output.close()
                
                

if __name__=="__main__":
    #crawl_song(URLS)
    crawl_lyrics()
    
