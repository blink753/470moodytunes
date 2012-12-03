# Some helper functions.
# You should not need to edit this file.

import ujson
import fileinput

def read_tweets(filename):
    for line in fileinput.input(filename):
        yield ujson.loads(line)

    
