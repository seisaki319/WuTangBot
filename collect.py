# adapted from bigishdata.com
import requests
import os, sys
import re
import config
from bs4 import BeautifulSoup

config = config.Config()
base_url = "http://genius.com"
headers = {'Authorization': 'Bearer {0}'.format(config.genius_api_key)}

def lyrics_from_song_api_path(song_api_path):
  #gotta go regular html scraping... come on Genius
  page_url = "http://genius.com" + song_api_path
  page = requests.get(page_url)
  html = BeautifulSoup(page.text, "html.parser")
  #remove script tags that they put in the middle of the lyrics
  [h.extract() for h in html('script')]
  #at least Genius is nice and has a tag called 'lyrics'!
  lyrics = html.find('div', class_='lyrics').get_text() #updated css where the lyrics are based in HTML
  return re.sub(r"\{.*\}", "", re.sub(r"\[.*\]", "", lyrics))

def lyrics_from_artists(artist_id):
  print('Rendering artist {0}'.format(artist_id))
  doc, response, i = "", "", 1
  while not response or response.json()['response']['songs']:
    print('Rendering page {0}'.format(i))
    response = requests.get("http://api.genius.com/artists/{0}/songs?per_page=50&page={1}".format(artist_id, i), headers = headers)
    for song in response.json()['response']['songs']:
      lyrics = lyrics_from_song_api_path(song['api_path'])
      doc += lyrics
    i += 1
  return doc
if __name__ == "__main__":
  artistid = sys.argv[1]
  artistname = sys.argv[2]
  doc = lyrics_from_artists(artistid).encode('ascii', 'ignore')
  with open(os.path.join('input','{0}.txt'.format(artistname)), 'wb') as f:
    f.write(doc)