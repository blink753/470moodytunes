# Some helper functions.
# You should not need to edit this file.

import ujson
import fileinput

def read_tweets():
    for line in fileinput.input():
        yield ujson.loads(line)
        
# def read_songs(filename):
    # json_file = open('training_set.json')
    # data = ujson.load(json_file)
    # json_file.close()
    # return data
    
def read_songs(filename):
    json_file = open('training_set.json')
    for line in iter(json_file):
        yield ujson.loads(line)
    json_file.close()
    