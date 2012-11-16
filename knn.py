song_list = []
training_set = []
k = 5

def knn():
    """
    purpose: 
    parameter:
    return: 
    """
    for song in song_list:
        cosine_list = []
        mood_count = collections.defaultdict(int)
        for train_song in training_set:
            cosine = sum(song['tfidf'][term]*train_song['tfidf'].get(term,0) for term in song['tfidf'])
            cosine_list.append({'mood':train_song['mood'], 'cosine':cosine})
        neighbors = sorted(cosine_list, key=lambda k: k['cosine'])[:k]
        for cosine_song in cosine_list:
            mood_count[cosine_song['mood']] = mood_count[cosine_song['mood']] + 1
        song_mood = max(mood_count, mood_count.get)
        song['mood'] = song_mood

if __name__=="__main__":
    knn()