import requests
import re
import time
from datetime import datetime

# function to clean synopsis
def _clean_synopsis(synopsis):
    # remove newlines
    synopsis = re.sub('\n', '', synopsis)
    # remove anything inside square brackets
    synopsis = re.sub('\[.*?\]', '', synopsis)
    return synopsis.strip()

# function to extract rating
def _extract_rating(rating):
    if rating is None:
        return 'Uknown'
    # split by the last occurrence of "-"
    split_index = rating.rfind('-')
    if split_index != -1:
        rating = rating[:split_index].strip()
    return rating

# function to format date
def _clean_date(date_str):
    return datetime.fromisoformat(date_str).strftime('%d %b %Y')

# parse multiple anime data from json
def parse_anime_data(data):
    anime_data = {}
    index=0
    for item in data['data']:
        anime = {}
        anime['anime_id'] = item['mal_id']
        anime['title'] = item.get('title', 'unknown')
        anime['title_japanese'] = item.get('title_japanese', 'unknown')
        anime['type'] = item.get('type', 'unknown')
        anime['image_url'] = item.get('images', {}).get('jpg', {}).get('large_image_url', 'unknown')
        anime['synopsis'] = _clean_synopsis(item.get('synopsis', 'unknown'))
        anime['episodes'] = item.get('episodes', 'unknown')
        anime['aire'] = item.get('aired', {}).get('string', 'unknown')
        anime['date'] = _clean_date(item.get('aired', {}).get('from', 'unknown'))
        anime['premiere'] = str(item.get('year', 'unknown')) + " " + (str(item.get('season', 'unknown'))).capitalize()
        anime['duration'] = item.get('duration', 'unknown')
        anime['source'] = item.get('source', 'unknown')
        anime['status'] = item.get('status', 'unknown')
        anime['rating'] = _extract_rating(item.get('rating', 'unknown'))
        anime['score'] = item.get('score', 'unknown')
        anime['scored_by'] = item.get('scored_by', 'unknown')
        anime['favorites'] = item.get('favorites', 'unknown')
        anime['studios'] = ', '.join([studio.get('name', 'unknown') for studio in item.get('studios', [])])
        anime['genres'] = ', '.join([genre.get('name', 'unknown') for genre in item.get('genres', [])])
        anime['themes'] = ', '.join([theme.get('name', 'unknown') for theme in item.get('themes', [])])
        anime['demographics'] = ', '.join([demo.get('name', 'unknown') for demo in item.get('demographics', [])])
        anime_data[index] = anime
        index+=1
    return anime_data

def parse_anime(item):
    anime = {}
    anime['anime_id'] = item['mal_id']
    anime['title'] = item.get('title', 'unknown')
    anime['title_japanese'] = item.get('title_japanese', 'unknown')
    anime['type'] = item.get('type', 'unknown')
    anime['image_url'] = item.get('images', {}).get('jpg', {}).get('large_image_url', 'unknown')
    anime['synopsis'] = _clean_synopsis(item.get('synopsis', 'unknown'))
    anime['episodes'] = item.get('episodes', 'unknown')
    anime['aire'] = item.get('aired', {}).get('string', 'unknown')
    anime['date'] = _clean_date(item.get('aired', {}).get('from', 'unknown'))
    anime['premiere'] = str(item.get('year', 'unknown')) + " " + (str(item.get('season', 'unknown'))).capitalize()
    anime['duration'] = item.get('duration', 'unknown')
    anime['source'] = item.get('source', 'unknown')
    anime['status'] = item.get('status', 'unknown')
    anime['rating'] = _extract_rating(item.get('rating', 'unknown'))
    anime['score'] = item.get('score', 'unknown')
    anime['scored_by'] = item.get('scored_by', 'unknown')
    anime['favorites'] = item.get('favorites', 'unknown')
    anime['studios'] = ', '.join([studio.get('name', 'unknown') for studio in item.get('studios', [])])
    anime['genres'] = ', '.join([genre.get('name', 'unknown') for genre in item.get('genres', [])])
    anime['themes'] = ', '.join([theme.get('name', 'unknown') for theme in item.get('themes', [])])
    anime['demographics'] = ', '.join([demo.get('name', 'unknown') for demo in item.get('demographics', [])])
    return anime


# fetch currentyly aring animes from Jikan
def fetch_currenty_airing():
    time.sleep(.2)
    response = requests.get('https://api.jikan.moe/v4/top/anime?filter=airing')
    data = response.json()
    return parse_anime_data(data)

# fetch popular animes from Jikan
def fetch_popular():
    time.sleep(.2)
    response = requests.get('https://api.jikan.moe/v4/top/anime?filter=bypopularity')
    data = response.json()
    return parse_anime_data(data)

# fetch popular animes from Jikan
def fetch_favorite():
    time.sleep(.2)
    response = requests.get('https://api.jikan.moe/v4/top/anime?filter=favorite')
    data = response.json()
    return parse_anime_data(data)


# ============================================ RECOMMENDATION OF ANIME ============================================
# fetch full anime details from jikan
def fetch_anime_full(anime_id):
    # Make the API request to retrieve anime details
    time.sleep(.2)
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}/full"
    response = requests.get(api_url)
    item = response.json()
    return item

# fetch 10 recommended animes for given anime
def fetch_recommendation(anime_id):
    # Make the API request to retrieve anime recommendations
    time.sleep(.2)
    api_url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
    response = requests.get(api_url)
    data = response.json()

    # Extract the mal_id values for the first 10 recommendations
    anime_data = {}
    index=0
    for entry in data['data'][:10]:
        time.sleep(0.2)
        item = fetch_anime_full(entry['entry']['mal_id'])['data']

        anime = parse_anime(item) # parse anime
        anime_data[index] = anime
        index+=1
    
    return anime_data
