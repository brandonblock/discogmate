import json
import requests
import sys

artist = sys.argv[1]
artist = artist.replace(' ', '+')
track = sys.argv[2]
track = track.replace(' ', '+')
key = "NUPJPAJpaqTecgraPvbn"
secret = "SnRHtnijQNkVIdvvcPvPAygHVsrkBUoL"


def fetch_release_data(release_id):

    url = "https://api.discogs.com/releases/%s?f=json&key=%s&secret=%s" % (release_id, key, secret)
    response = requests.get(url)
    response.raise_for_status()

    releasejson = json.loads(response.text)

    have = releasejson['community']['have']
    want = releasejson['community']['want']
    rating = releasejson['community']['rating']['average']
    rateCount = releasejson['community']['rating']['count']
    return have, want, rating, rateCount


def search_releases(artist, track):
    url = "https://api.discogs.com/database/search?type=release&artist=%s&label=&track=%s&advanced=1&key=%s&secret=%s" % (artist, track, key, secret)
    response = requests.get(url)
    response.raise_for_status()

    resultsjson = json.loads(response.text)
    i = 0
    for label in resultsjson['results']:
        print(resultsjson['results'][i]['id'])
        print(fetch_release_data(resultsjson['results'][i]['id']))
        i += 1


search_releases(artist, track)

