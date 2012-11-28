This is the progject for csce 470. It is an application that allows a user to find songs based on their mood
by analyzing the words in songs that have a similar mood and and comparing them to popular and recognizable songs.

These are the files:
.gitignore - list of files for git to ignore
README.txt - this file
crawl.py - the script that crawls azlyrics.com for song lyrics
crawl1.py - the script that crawls chartlyrics.com for song lyrics that are not found on azlyrics.com
knn.py - our core algorithm that calculates the knn for songs
knn_tests.py - the script taht is called to test the knn algorithm
top_songs.json - a list of artists and songs from iTunes that is read by the crawlers to know what to search for
training_set.json - the file that holds the songs for out training set
lyrics.json - the file that holds all of the lyrics that we collected so far
utils.py - some simple utilities


To run the crawlers you will need to install the following modules:

pip install beautifulsoup4

pip install feedparser

pip install unidecode

pip install xml

pip install ast

pip install codecs

**NOTE**: crawl.py will need to be run first before running crawl1.py 

To run our crawlers just run: $ crawl.py
                              $ crawl1.py

To run our tests just run: $ knn_tests.py