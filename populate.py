from datetime import datetime

import requests
from model import *


band_ids = [
    '3WrFJ7ztbogyGnTHbHJFl2',
    '22bE4uQ6baNwSHPVcDxLCe',
    '70cRZdQywnSFp9pnc2WTCE',
    '3AA28KZvwAUcZuOKwyblJQ',
    '3jOstUTkEu2JkjvRdBA5Gu',
]


def load_artist(artist_id):
    response = requests.get('https://api.spotify.com/v1/artists/{}'.format(artist_id))
    band = Band(name=response.json()['name'])
    session.add(band)
    load_albums(band, artist_id)


def load_albums(band, artist_id):
    response = requests.get('https://api.spotify.com/v1/artists/{}/albums?album_type=album&market=US'.format(artist_id))
    data = response.json()

    for album_item in data['items']:
        if len(album_item['artists']) > 1:
            continue
        response = requests.get(album_item['href'])
        album_data = response.json()
        album = Album(
            title=album_data['name'],
            band=band
        )
        if album_data['release_date_precision'] == 'day':
            album.release_date = datetime.strptime(album_data['release_date'], '%Y-%m-%d').date()
        session.add(album)

        load_tracks(album, album_data['tracks']['items'])


def load_tracks(album, track_list):
    for track_data in track_list:
        song = Song(
            title=track_data['name'],
            track_num=track_data['track_number'],
            length_seconds=track_data['duration_ms'] / 1000.0,
            album=album
        )
        session.add(song)


for band_id in band_ids:
    load_artist(band_id)

session.commit()
