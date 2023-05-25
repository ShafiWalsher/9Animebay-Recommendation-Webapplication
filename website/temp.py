# import requests
# import re
# import time

# # function to clean synopsis
# def clean_synopsis(synopsis):
#     # remove newlines
#     synopsis = re.sub('\n', '', synopsis)
#     # remove anything inside square brackets
#     synopsis = re.sub('\[.*?\]', '', synopsis)
#     return synopsis.strip()

# # function to extract rating
# def extract_rating(rating):
#     # split by the last occurrence of "-"
#     split_index = rating.rfind('-')
#     if split_index != -1:
#         rating = rating[:split_index].strip()
#     return rating



# def parse_anime(item):
#     anime = {}
#     anime['anime_id'] = item['mal_id']
#     anime['title'] = item.get('title', 'unknown')
#     anime['title_japanese'] = item.get('title_japanese', 'unknown')
#     anime['type'] = item.get('type', 'unknown')
#     anime['image_url'] = item.get('images', {}).get('jpg', {}).get('large_image_url', 'unknown')
#     anime['synopsis'] = clean_synopsis(item.get('synopsis', 'unknown'))
#     anime['episodes'] = item.get('episodes', 'unknown')
#     anime['duration'] = item.get('duration', 'unknown')
#     anime['status'] = item.get('status', 'unknown')
#     anime['rating'] = extract_rating(item.get('rating', 'unknown'))
#     anime['score'] = item.get('score', 'unknown')
#     anime['scored_by'] = item.get('scored_by', 'unknown')
#     anime['favorites'] = item.get('favorites', 'unknown')
#     anime['studios'] = ', '.join([studio.get('name', 'unknown') for studio in item.get('studios', [])])
#     anime['genres'] = ', '.join([genre.get('name', 'unknown') for genre in item.get('genres', [])])
#     anime['themes'] = ', '.join([theme.get('name', 'unknown') for theme in item.get('themes', [])])
#     anime['demographics'] = ', '.join([demo.get('name', 'unknown') for demo in item.get('demographics', [])])
#     return anime


# # fetch full anime details from jikan
# def fetch_anime_full(anime_id):
#     # Make the API request to retrieve anime details
#     time.sleep(.2)
#     api_url = f"https://api.jikan.moe/v4/anime/{anime_id}/full"
#     response = requests.get(api_url)
#     item = response.json()
#     return item

# def fetch_recommendation(anime_id):
#     # Make the API request to retrieve anime recommendations
#     time.sleep(.2)
#     api_url = f"https://api.jikan.moe/v4/anime/{anime_id}/recommendations"
#     response = requests.get(api_url)
#     data = response.json()

#     # Extract the mal_id values for the first 10 recommendations
#     anime_data = {}
#     index=0
#     for entry in data['data'][:10]:
#         time.sleep(0.2)
#         item = fetch_anime_full(entry['entry']['mal_id'])['data']

#         anime = parse_anime(item) # parse anime
#         anime_data[index] = anime
#         index+=1
#         anime_data.update(anime)
    
#     return anime_data

# # print(parse_anime(fetch_anime_full(1)['data']))
# print(fetch_recommendation(1))


# # print(anime_details)


# from datetime import datetime

# # input date string
# date_str = '2023-04-12T00:00:00+00:00'

# # create datetime object from the input string
# datetime.fromisoformat(date_str).strftime('%d %b %Y')

# print(datetime.fromisoformat(date_str).strftime('%d %b %Y')) # output: 12 Apr 2023



from fuzzywuzzy import process
import os
import pandas as pd


_base_dir = os.path.abspath(os.path.dirname(__file__))
_dataset_dir = os.path.join(_base_dir, 'static', 'datasets')
_anime_csv = os.path.join(_dataset_dir, 'animes.csv')

anime_dataset = pd.read_csv(_anime_csv)

# print (anime_dataset.columns)

query = 'one punch man' #request.args.get('q', '').strip()

if len(query) >= 3:
    # Filter the dataframe based on the input query
    filtered_anime_data = anime_dataset[anime_dataset['title'].str.contains(query, case=False)][:5]

    # Return the filtered rows as a list of dictionaries
    search_results = filtered_anime_data.to_dict('records')
else:
    search_results = []

print(search_results)

