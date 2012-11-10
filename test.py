#simple test get from azlyrics

import urllib

#get lyrics for a song
response = urllib.urlopen("http://www.azlyrics.com/lyrics/katyperry/ifyoucanaffordme.html")
text = response.read()

startpos = text.find("!-- start of lyrics")
startl = startpos+len("!-- start of lyrics")
endpos = text.find("!-- end of lyrics")

lyrics = text[startl+4:endpos-3]
lyrics = lyrics.replace('<br />','')
lyrics = lyrics.replace('\r\n','')

print(lyrics)


#getting artists
"""
start with urllib.urlopen("http://www.azlyrics.com/[a-z,19(for the #)]
    in each of the lists 
        find: <div class="artists fl">
        then find: <br /><br /> before it
        find: </div> after it to get the list of artists
"""

response = urllib.urlopen("http://www.azlyrics.com/a.html")
page=response.read()
artist_start = page.rfind("<br /><br />")
artists_middle = page.rfind('<div class="artists fl">')
artists_end = page.find("</div>,artists_middle,len(page)")
page_artists = page[artist_start:artists_end]
artists = page_artists[page_artists.find("a href=")+8:len(page_artists)]
artist_list = artists.split('<a href="')
for each_artist in artist_list:
    
    artist_url = each_artist[0:each_artist.find('"')]

#getting songs
"""
for each artist found above
    find: var songlist
        each song surrounded by {}
    till: a:""}];
"""
#pass [artist] in from getting artists ex: k/keithanderson.html
artist = "k/keithanderson.html"
url = "http://www.azlyrics.com/"
url+=artist
#response = urllib.urlopen("http://www.azlyrics.com/b/blink.html")
response = urllib.urlopen(url)
songpage = response.read()
begin_songlist=songpage.find("songlist")
end_songlist=songpage.find("var res")
#songs = songpage[begin_songlist+(text.find('{',begin_songlist)-begin_songlist)+1:end_songlist]
songs = songpage[begin_songlist+(songpage.find('{',begin_songlist)-begin_songlist)+1:end_songlist]
songlist=songs.split('{')

for every song in songlist:
    spot = song.find('h:"..')+len('h:"..')
    song_url = song[spot:song.find('"',spot)]
