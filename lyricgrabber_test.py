import lyricgrabber
import string
import time
start_time = time.time()
filename = "lyriclist"
f = open('lyriclistA.txt','w')
f.close()
output = open('lyrics.json', 'w')
output.close()

#get artist


#go through just artists with the letter a 
lyricgrabber.getartists('a')
end_time = time.time()
print 'done with lyric crawl after %.3f seconds'%(end_time-start_time)

#go through all the letters
"""
for letter in string.lowercase:
    lyricgrabber.getartists(letter)
end_time = time.time()
print 'done with lyric crawl after %.3f seconds'%(end_time-start_time)
"""