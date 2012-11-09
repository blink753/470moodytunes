#simple test get from azlyrics

import urllib
response = urllib.urlopen("http://www.azlyrics.com/lyrics/katyperry/ifyoucanaffordme.html")
text = response.read()

startpos = text.find("!-- start of lyrics")
endpos = text.find("!-- end of lyrics")

lyrics = text[startpos:endpos]

print(lyrics)