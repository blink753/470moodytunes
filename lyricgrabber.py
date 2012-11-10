import urllib
import time

def getartists(letter):
    #letter = 'a'
    url = "http://www.azlyrics.com/"+letter+".html"
    #response = urllib.urlopen("http://www.azlyrics.com/a.html")
    time.sleep(random.randrange(1,3))
    response = urllib.urlopen(url)
    page=response.read()
    artist_start = page.rfind("<br /><br />")
    artists_middle = page.rfind('<div class="artists fl">')
    artists_end = page.find("</div>,artists_middle,len(page)")
    page_artists = page[artist_start:artists_end]
    artists = page_artists[page_artists.find("a href=")+8:len(page_artists)]
    artist_list = artists.split('<a href="')
    for each_artist in artist_list:
        artist_url = each_artist[0:each_artist.find('"')]
        if(artist_url.find('http:')== -1):
            #call getsongs(artist_url)
            getsongs(artist_url)
            #print(artist_url)
    return
    
def getsongs(artist_url):
    #artist_url = "k/keithanderson.html"
    url = "http://www.azlyrics.com/"
    url+=artist_url
    #response = urllib.urlopen("http://www.azlyrics.com/b/blink.html")
    time.sleep(random.randrange(1,3))
    response = urllib.urlopen(url)
    songpage = response.read()
    begin_songlist=songpage.find("songlist")
    end_songlist=songpage.find("var res")
    #songs = songpage[begin_songlist+(text.find('{',begin_songlist)-begin_songlist)+1:end_songlist]
    songs = songpage[begin_songlist+(songpage.find('{',begin_songlist)-begin_songlist)+1:end_songlist]
    songlist=songs.split('{')
    for song in songlist:
        spot = song.find('h:"..')+len('h:"..')
        song_url = song[spot:song.find('"',spot)]
        if(song_url.find('http:')== -1):
            #call getlyrics(song_url)
            getlyrics(song_url)
            #print(song_url)
    return
    
def getlyrics(song_url):
    #song_url = "/lyrics/keithanderson/adaliene.html"
    url = "http://www.azlyrics.com"+song_url
    #response = urllib.urlopen("http://www.azlyrics.com/lyrics/katyperry/ifyoucanaffordme.html")
    time.sleep(random.randrange(5,10))
    response = urllib.urlopen(url)
    text = response.read()
    startpos = text.find("!-- start of lyrics")
    startl = startpos+len("!-- start of lyrics")
    endpos = text.find("!-- end of lyrics")
    lyrics = text[startl+4:endpos-3]
    lyrics = lyrics.replace('<br />','')
    lyrics = lyrics.replace('\r\n','')
    f = open('lyriclistA.txt','a')
    f.write(song_url+"\r\n")
    f.write("\r\n")
    f.write(lyrics+"\r\n")
    f.write("\r\n")
    f.close()
    
    return
    