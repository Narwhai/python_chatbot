import requests, sys
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer' +  'cAJ6W_b5hYAbi0lswe4JwRCb7Ak4-tDnMgy8fViObYRQuVwbhcNJtC30hBQm7HV6'}

song_title = ""
artist_name = ""

defaults = {
    'request': {
        'token': 'cAJ6W_b5hYAbi0lswe4JwRCb7Ak4-tDnMgy8fViObYRQuVwbhcNJtC30hBQm7HV6',
        'base_url': 'https://api.genius.com'
    },
    'message': {
        'search_fail': 'I couldn\'t find the lyrics for that song :(',
    }
}


# Pulls song information from Genius, returns a URL from which lyrics can be scrapped
def request_song_info(song_title, artist_name):
    base_url = defaults['request']['base_url']
    headers = {'Authorization': 'Bearer ' + defaults['request']['token']}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response


# Scraps lyrics from the URL found 
def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics


# Calls the other functions to ultimately get the requested song lyrics and return them
def get_lyrics(song_title, artist_name):

    # Search for matches in request response
    response = request_song_info(song_title, artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break

    # If song is found, extracts lyrics from URL
    if remote_song_info:
        song_url = remote_song_info['result']['url']
        lyrics = scrap_song_url(song_url)

        response = ("Here are the lyrics for: " + song_title.capitalize() + " by " + artist_name)
        response += lyrics
        return response

    else:
        response = defaults['message']['search_fail']
        return response