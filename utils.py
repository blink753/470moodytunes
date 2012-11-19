# Some helper functions.
# You should not need to edit this file.

import ujson
import fileinput

def read_tweets():
    for line in fileinput.input():
        yield ujson.loads(line)