from flask import Blueprint, render_template, request, redirect, url_for
from .jikan_api import fetch_anime_full, fetch_currenty_airing, fetch_popular, fetch_favorite, fetch_recommendation, parse_anime
from .recommend import get_ncf_recommendations, get_bpr_recommendations

# parallel api requests
import concurrent.futures


routes = Blueprint('routes',__name__)


@routes.route('/')
def index():
    return render_template("index.html")

@routes.route('/home')
@routes.route('/anime')
def home():
    airing_animes = fetch_currenty_airing()
    popular_animes = fetch_popular()
    return render_template("home.html", airing_animes=airing_animes, popular_animes=popular_animes)

# Serach Funtionality
# @routes.route('/searchanime', methods=['GET', 'POST'])
# def search():
#     if request.method == 'POST':
#         query = (request.form['query']).strip()

#         if len(query) >= 3:
#             # Filter the dataframe based on the input query
#             filtered_anime_data = anime_dataset[anime_dataset['title'].str.contains(query, case=False)]
#             # Return the filtered rows as a list of dictionaries
#             search_results = filtered_anime_data.to_dict('records')
#             print('SHAFI WALSHER:  ', search_results)
#         else:
#             search_results = []

#     return jsonify({'htmlresponse': render_template('search-results.html', search_results=search_results)})


@routes.route('/project-details')
def project_details():
    return render_template("project-details.html")

@routes.route('/results')
def results():
    return render_template("results.html")

@routes.route('/about-us')
def about():
    return render_template("about.html")


@routes.route('/test')
def test():
    return render_template("test.html")

# Anime Page Route
@routes.route('/anime/<int:anime_id>')
def anime(anime_id):
    anime_details = parse_anime(fetch_anime_full(anime_id)['data'])
    fav_animes = fetch_favorite()
    reco_animes = fetch_recommendation(anime_id)
    return render_template("anime.html", anime_details=anime_details, fav_animes=fav_animes, reco_animes=reco_animes)


# NCF BPR Recommendation Route
@routes.route('/recommend', methods=['GET','POST'])
@routes.route('/recommendation', methods=['GET','POST'])
def recommend():
    # TOTAL No OF USERS: 73516
    reco_animes = {}
    user_id = None
    model_type = None
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        model_type = request.form.get('model_type')

        if user_id <= 73516:
            if model_type == 'NCF':
                reco_animes_ids = get_ncf_recommendations(user_id)
            if model_type == 'BPR':
                reco_animes_ids = get_bpr_recommendations(user_id)
        else:
            reco_animes_ids = []
        if reco_animes_ids is not None:
            index=0
            for anime_id in reco_animes_ids:
                anime = parse_anime(fetch_anime_full(anime_id)['data'])
                reco_animes[index] = anime
                index+=1

    return render_template("recommend.html", reco_animes=reco_animes, user_id=user_id, model_type=model_type)


