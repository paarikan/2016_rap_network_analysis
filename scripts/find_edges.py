import requests
import urllib
import json
import io
import sys

def main():
    artist_pair_counts = get_artist_pair_counts()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    o = open('../data/artist_pair_counts.csv', 'w')
    for artist_pair_frozenset in artist_pair_counts:
        artist_pair = list(artist_pair_frozenset)
        if len(artist_pair) > 1:
            o.write(artist_pair[0] + ',')
            o.write(artist_pair[1] + ',')
            o.write(str(artist_pair_counts[artist_pair_frozenset]/2).encode('utf8') + '\n')

    o.close()

def get_artist_pair_counts():
    f = open('../data/billboard_rap_chart_albums_cleaned.csv')
    artist_pair_counts = {}
    i = 1
    for line in f:
        tokens = line.split(',')
        album_name = tokens[0]
        artist_name = tokens[1]
        album_id = find_album(album_name, artist_name)
        tracks = get_tracks(album_id)
        for track in tracks:
            artists = get_artists(track)
            for artist in artists:
                for artist2 in artists:
                    artist_pair = frozenset([artist,artist2])
                    artist_pair_count = artist_pair_counts.get(artist_pair, 0)
                    artist_pair_counts[artist_pair] = artist_pair_count + 1

        print i
        i = i+1

    return artist_pair_counts

def get_artists(track_id):
    base_url = 'https://api.spotify.com/v1/tracks/'
    response = requests.get(base_url+track_id)
    response_dict = json.loads(response.text)
    artists = []
    for artist in response_dict['artists']:
        artists.append(artist['name'])
    return artists

def get_tracks(album_id):
    base_url = 'https://api.spotify.com/v1/albums/'
    response = requests.get(base_url+album_id)
    response_dict = json.loads(response.text)
    ids = []
    for track in response_dict['tracks']['items']:
        ids.append(track['id'])
    return ids

def find_album(album_name, artist_name):
    search_url = 'https://api.spotify.com/v1/search?q=album:{}%20artist:{}&type=album'.format(urllib.quote_plus(album_name),urllib.quote_plus(artist_name))
    response = requests.get(search_url)
    response_dict = json.loads(response.text)
    found_album = response_dict['albums']['items'][0]
    return found_album['id']
    
if __name__ == "__main__":
    main()