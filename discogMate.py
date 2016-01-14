import json
import requests
import sys
import time

# This script gleans stats from discogs.com and returns an array:
# [release ID, year, format, ratings, rate count, have, want]

artist = sys.argv[1]
artist = artist.replace(' ', '+')
track = sys.argv[2]
track = track.replace(' ', '+')
key = "NUPJPAJpaqTecgraPvbn"  # digirithm's Discogs user key
secret = "SnRHtnijQNkVIdvvcPvPAygHVsrkBUoL"  # digirithm's user secret
rate_limit = .25  # 250 requests per minute/once every 240 milliseconds


# This method takes a release ID and grabs/instantiates a JSON object with it.
def fetch_release_data(release_id):
    url = "https://api.discogs.com/releases/%s?f=json&key=%s&secret=%s" % (release_id, key, secret)
    response = requests.get(url)
    response.raise_for_status()

    releasejson = json.loads(response.text)

    year = releasejson['year']
    formats = releasejson['formats'][0]['name']
    rating = releasejson['community']['rating']['average']
    rateCount = releasejson['community']['rating']['count']
    have = releasejson['community']['have']
    want = releasejson['community']['want']

    return year, formats, rating, rateCount, have, want


# This method performs a search for all releases and grabs JSON object from each
def search_releases(artist, track):
    url = "https://api.discogs.com/database/search?type=release&artist=%s&label=&track=%s&advanced=1&key=%s&secret=%s" \
          % (artist, track, key, secret)
    response = requests.get(url)
    response.raise_for_status()
    resultsjson = json.loads(response.text)

    output_array = []
    i = 0
    for label in resultsjson['results']:
        result_array = []
        result_array.append(resultsjson['results'][i]['id'])
        for result in fetch_release_data(resultsjson['results'][i]['id']):
            result_array.append(result)

        output_array.append(result_array)
        i += 1
        time.sleep(rate_limit)

    for item in output_array:
        print(item)


search_releases(artist, track)


