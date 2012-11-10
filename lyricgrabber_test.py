import lyricgrabber
import string
import time
start_time = time.time()
f = open('lyriclist.txt','w')
f.close()

for letter in string.lowercase:
    lyricgrabber.getartists(letter)
end_time = time.time()
print 'done with sentiment after %.3f seconds'%(end_time-start_time)