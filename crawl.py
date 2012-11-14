#!/usr/bin/env python
import ast
from bs4 import BeautifulSoup
from collections import defaultdict
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
    rul = "|\([^)]*\)"
    name = ""
    # Removing extra description
    trimmed = re.sub('\[[^]]*\]', '', song.lower())
    tokens = re.split(' ', trimmed)
    for token in tokens:
        if token == '':
            continue
        else:
            name = name + token + ' '

    return name[:len(name)-1]

def split_multiple_artist(name):

    names = ""
    sep = re.findall('[\w.+ ]+', name)
    first_artist = re.split(' ', sep[0])
    
    for token in first_artist:
        if token == '':
            continue
        else:
            names = names + token + ' '

    return names[:len(names)-1]

def apostrophe(name):

    names = ""
    sep = re.findall('[\w+]+', name)
    
    for token in sep:
        if token == '':
            continue
        else:
            names = names + token + ' '

    return names[:len(names)-1]
    
def getlyrics(response):
    if response.getcode() == 200:
        text = response.read()
        startpos = text.find("!-- start of lyrics")
        startl = startpos+len("!-- start of lyrics")
        endpos = text.find("!-- end of lyrics")
        lyrics = text[startl+4:endpos-3]
        lyrics = lyrics.replace('<br />','')
        lyrics = lyrics.replace('\r\n','')
        while (lyrics.find('<i>')!=-1):
            startstrip=lyrics.find('<i>')
            endstrip=lyrics.find('</i>',startstrip)+4
            lyrics = lyrics[:startstrip]+lyrics[endstrip:]
    else:
        lyrics = ""

    return lyrics

def crawl_song(rss_feed):
    """
    purpose: crawl up to the top 300 songs for different genres from rss feeds.
    parameter:
        `rss_feed`: a list of rss feeds urls.
    return: None.

    """

    total_output = open('top_songs.json', 'w')
    total = {}
    for url in rss_feed:
        feed = feedparser.parse(url['url'])
        output = open('top_songs.%s.json'%url['genre'], 'w')
        # checking if url is a well-formed xml
        if feed['bozo']!=1:
            for item in feed['items']:
                title_artist = split(item['title'])
                artist = title_artist[1]
                song = {'title': split_song_title(title_artist[0]), 'artist': unidecode(unicode(title_artist[1]))}
                if split_song_title(title_artist[0]) not in total:
                    total[split_song_title(title_artist[0])] = unidecode(unicode(title_artist[1]))
                output.write(str(json.dumps(song)) + "\n")
                
        output.close()
        
    for song in total:
        s = {'title': song, 'artist': total[song]}
        total_output.write(str(json.dumps(s)) + "\n")
        
    total_output.close()

def drop_stop_word(name):
    """
    purpose: helper function dropping "The" in artist's name
    parameter:
            `name`: artist's name
    return: trimmed artitst's name

    """
    if name[:4] == "the ":
        tokens = re.sub(name[:4], '', name)
        return tokens
    else:
        return name

def url_handler(fail_output, response, song_dict):

    #fail_output = open('not_found.%s.json'%url, 'w')
    s = {'title': song_dict['title'], 'lyrics': "", 'status': response.getcode(), 'artist': song_dict['artist']}
    fail_output.write(str(json.dumps(s)) + "\n")
    response.close()
    time.sleep(5)
    
def crawl_lyrics(rss_feed):
    """
    purpose: crawl the lyrics for up to the top 300 songs for each genre based on rss feeds
    paramemter:
            `rss_feed`: a list of rss feed urls
    return: None

    """
    count = 0
    for url in rss_feed:
        reader = open('top_songs.%s.json'%url['genre'], 'r')
        output = open('lyrics.%s.json'%url['genre'], 'w')
        fail_output = open('not_found.%s.json'%url['genre'], 'w')
        count = 0
        for line in iter(reader):
            song_dict = ast.literal_eval(line)
            #dropping "the" in artist name
            trimmed_artist_name = drop_stop_word(song_dict['artist'])
            if '&' in trimmed_artist_name:
                trimmed_artist_name = split_multiple_artist(trimmed_artist_name)

            if trimmed_artist_name[0].isdigit():
                artists_url = "http://www.azlyrics.com/19.html"
            else:
                artists_url = "http://www.azlyrics.com/%s.html" % (trimmed_artist_name[0])

            page = urllib.urlopen(artists_url)
            if page.getcode() == 200:
                soup = BeautifulSoup(page.read())
                divs_right = soup.find('div', attrs = {'class': 'artists fr'})
                divs_left = soup.find('div', attrs = {'class': 'artists fl'})
                available_names = []
                page.close()
                links = {}

                if divs_right:
                    link_list_right = divs_right.find_all('a')
                    for link in link_list_right:
                        if '\'' in link.text.lower():
                            stripped_name = apostrophe(link.text.lower())
                        else:
                            stripped_name = link.text.lower()
                        links[stripped_name] = link.get('href')
                        available_names.append(stripped_name)
                        
                if divs_left:
                    link_list_left = divs_left.find_all('a')
                    for link in link_list_left:
                        if '\'' in link.text.lower():
                            stripped_name = split_multiple_artist(link.text.lower())
                        else:
                            stripped_name = link.text.lower()
                            
                        links[stripped_name] = link.get('href')
                        available_names.append(stripped_name)
                        
                artist_count = 0
                
                for name in available_names:
                    #print trimmed_artist_name, "==", name
                    #print trimmed_artist_name[0], name[0], trimmed_artist_name[-1], name[len(trimmed_artist_name)-1]
                    if (trimmed_artist_name in name) and (trimmed_artist_name[0]==name[0])\
                       and (trimmed_artist_name[-1] == name[len(trimmed_artist_name)-1]) and ' - ' not in name:
                        print "artist found = ", trimmed_artist_name, "--OR--", name
                        if "http://www" in links[name]:
                             song_list_url = links[name]
                        else:
                            song_list_url = "http://www.azlyrics.com/%s" % (links[name])
                        page1 = urllib.urlopen(song_list_url)
                        print song_list_url
                        #jumping to artist's songs page
                        if page1.getcode() == 200:
                            soup = BeautifulSoup(page1.read())
                            songs = soup.find_all('a', attrs = {'target': '_blank'})
                            page1.close()
                            lyrics_links = {}
                            for song in songs:
                                lyrics_links[song.text.lower()] = song.get('href')[2:]

                            count = 0
                            for song in lyrics_links:
                                length = len(song)
                                if (song in song_dict['title']) and (song[0] == song_dict['title'][0])\
                                   and (song[length-1] == song_dict['title'][length-1])\
                                   and ("www" not in lyrics_links[song]):
                                    lyrics_url = "http://www.azlyrics.com"+lyrics_links[song]
                                    print "lyrics found: ", song, "==", song_dict['title'], "==>", lyrics_url
                                    page2 = urllib.urlopen(lyrics_url)
                                    if page2.getcode() == 200:
                                        lyrics = getlyrics(page2)
                                        page2.close()
                                        
                                        s = {'title': song, 'lyrics': lyrics, 'artist': song_dict['artist']}
                                        output.write(str(json.dumps(s)) + "\n")

                                        print "sleeping"
                                        time.sleep(10)
                                        count = 0
                                        break
                                    else:
                                        print "fail opening lyrics page"
                                        url_handler(fail_output, page2, song_dict)
                                else:
                                    count +=1

                            if count == len(lyrics_links):
                                print "song not found", song_dict
                                fail_output.write(str(json.dumps(song_dict)) + "\n")
                            else:
                                break
                        # Fail opening an artist's list of songs url
                        else:
			    print "Fail opening an artist's list of songs url"
                            url_handler(fail_output, page1, song_dict)
                    else:
                        artist_count +=1
                        
                if artist_count == len(available_names):
                    print "artist not found ", song_dict
                    fail_output.write(str(json.dumps(song_dict)) + "\n")

	    # Fail opening list of artists url
            else:
		print "Fail opening list of artists url"
                url_handler(fail_output, page, song_dict)

	# Finish crawling a genre's lyrics
        reader.close()
        output.close()
        fail_output.close()


if __name__=="__main__":
    #crawl_song(URLS)
    crawl_lyrics(URLS)
