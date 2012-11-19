import urllib
import time
import utils
import string

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
    """
    split artist list in half
    split_num = len(artist_list)/2
    part1 = artist_list[:split_num]
    part2 = artist_list[split_num:]
    """
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
    
def getlyrics(songs):
    #song_url = "/lyrics/keithanderson/adaliene.html"
    url = "http://www.azlyrics.com"+song_url
    #response = urllib.urlopen("http://www.azlyrics.com/lyrics/katyperry/ifyoucanaffordme.html")
    #look at utils and see how amny 200 or 400 I got
    response = urllib.urlopen(url)
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
    #output = open('lyrics.json', 'a')
    #song = {'title': title_artist[0], 'artist': title_artist[1]}
    #output.write(str(json.dumps(song)) + "\n")
    
    
    f = open('toplyriclist.txt','a')
    f.write(song_url+"\r\n")
    f.write("\r\n")
    f.write(lyrics+"\r\n")
    f.write("\r\n")
    f.close()
    
if __name__=="__main__":
    start_time = time.time()
    songs = utils.read_tweets()
    #read in tweets from top_lyrics using utils
    #get artist and name
    testf = open('topsongstest.txt','w')
    for song in songs:
        artist = song["artist"]
        title = song["title"]
        #song_url = "/lyrics/keithanderson/adaliene.html"
        #artist = artist.replace(' ','')
        if(artist.find('(')!=-1):
            artist=artist[:artist.find('(')-1]
        artist = ''.join(ch for ch in artist if ch.isalnum())
        #title = title.replace(' ','')
        if(title.find('(')!=-1):
            title=title[:title.find('(')-1]
        title = ''.join(ch for ch in title if ch.isalnum())
        artist = filter(lambda x: x in string.printable, artist)
        title = filter(lambda x: x in string.printable, title)
        testf.write('{"artist": '+artist+', "title": '+title+'}\n')
        songurl = '/lyrics/'+artist+'/'+title+'.html'
        testf.write(songurl+'\n')
    
    testf.close()
    end_time = time.time()
    print 'done with lyric grabbing after %.3f seconds'%(end_time-start_time)
    pass

    