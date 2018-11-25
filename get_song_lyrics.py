import requests, sys
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {'Authorization': 'Bearer' +  'cAJ6W_b5hYAbi0lswe4JwRCb7Ak4-tDnMgy8fViObYRQuVwbhcNJtC30hBQm7HV6'}

song_title = "Lake Song"
artist_name = "The Decemberists"

defaults = {
    'request': {
        'token': 'cAJ6W_b5hYAbi0lswe4JwRCb7Ak4-tDnMgy8fViObYRQuVwbhcNJtC30hBQm7HV6',
        'base_url': 'https://api.genius.com'
    },
    'message': {
        'search_fail': 'The lyrics for this song were not found!',
        'wrong_input': 'Wrong number of arguments.\n' \
                       'Use two parameters to perform a custom search ' \
                       'or none to get the song currently playing on Spotify.'
    }
}

def request_song_info(song_title, artist_name):
    base_url = defaults['request']['base_url']
    headers = {'Authorization': 'Bearer ' + defaults['request']['token']}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

def main():
    # TODO fix this up a bit, get song name from user input, artist will always be Frank
    # Return error message if song not found 
    args_length = len(sys.argv)
    print(args_length)
    song_info = sys.argv
    song_title, artist_name = song_info[1], song_info[2]
    #else:
        #print(defaults['message']['wrong_input'])
        #return

    print('{} by {}'.format(song_title, artist_name))

    # Search for matches in request response
    response = request_song_info(song_title, artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break

    # Extract lyrics from URL if song was found
    if remote_song_info:
        song_url = remote_song_info['result']['url']
        lyrics = scrap_song_url(song_url)

        #write_lyrics_to_file(lyrics, song_title, artist_name)

        print(lyrics)
    else:
        print(defaults['message']['search_fail'])

if __name__ == '__main__':
    main()

"""
def lyrics_from_song_api_path(song_api_path):
    song_url = base_url + song_api_path
    response = requests.get(song_url, headers=headers)
    json = response.json()
    path = json["response"]["song"]["path"]
    #gotta go regular html scraping... come on Genius
    page_url = "http://genius.com" + path
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("div", class_="lyrics").get_text() #updated css where the lyrics are based in HTML
    return lyrics


if __name__ == "__main__":
    print("hewwo")
    search_url = base_url + "/search"
    data = {'q': song_title}
    response = requests.get(search_url, data=data, headers=headers)
    json = response.json()
    song_info = None
    for hit in json["response"]["hits"]:
        if hit["result"]["primary_artist"]["name"] == artist_name:
            song_info = hit
            break
    if song_info:
        song_api_path = song_info["result"]["api_path"]
        lyrics = lyrics_from_song_api_path(song_api_path)
        print(lyrics)
        print(lyrics_from_song_api_path(song_api_path))
"""