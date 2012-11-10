#simple test get from azlyrics

import urllib

#get lyrics for a song
response = urllib.urlopen("http://www.azlyrics.com/lyrics/katyperry/ifyoucanaffordme.html")
text = response.read()

startpos = text.find("!-- start of lyrics")
endpos = text.find("!-- end of lyrics")

lyrics = text[startpos:endpos]

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
page_artists = text[artist_start:artists_end]
artists = page_artists[page_artists.find("a href=")+8:len(page_artists)]
artisit_list = artists.split('<a href="')


#getting songs
"""
for each artist found above
    find: var songlist
        each song surrounded by {}
    till: a:""}];
"""

response = urllib.urlopen("http://www.azlyrics.com/b/blink.html")
songpage = response.read()
begin_songlist=songpage.find("songlist")
end_songlist=songpage.find("var res")
songs = songpage[begin_songlist+(text.find('{',begin_songlist)-begin_songlist)+1:end_songlist]
songlist=songs.split('{')
