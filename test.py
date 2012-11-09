#simple test get from azlyrics

import urllib
response = urllib.urlopen("http://www.azlyrics.com/lyrics/katyperry/ifyoucanaffordme.html")
response.read()