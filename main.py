from fastapi import FastAPI , Request , Form , File , UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from datetime import date
from fetch import movie, movie_collection
import pandas as pd
from ml import RECOMMAND
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")


df = pd.read_csv('datasets/tmdb.csv', encoding='utf-8')
all_titles = [df['title'][i] for i in range(len(df['title']))]


@app.get('/' , response_class=HTMLResponse)
def index(request: Request , search: str = Form(...)):
    
    year = date.today.year
    year_url = f'http://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&primary_release_year={year}&sort_by=popularity.desc'
    result = json.loads(requests.get('https://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&primary_release_year=2022&sort_by=popularity.desc').text)
    # print(result['results'][1])
    top_year = movie_collection()
    top_year.results=[]
    top_year.fetch(year_url)
    genre_url =f'https://api.themoviedb.org/3/genre/movie/list?api_key=da396cb4a1c47c5b912fda20fd3a3336&language=en-US'
    genres = json.loads(requests.get(genre_url).text)
    # print(genres)
    top_genre_collection = []
    for data in genres['genres']:
        # print(data['id'])
        genre_id = f'https://api.themoviedb.org/3/discover/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&with_genres={data["id"]}&sort_by=popularity.desc'
        # print(genre_id)
        top_genre = movie_collection()
        top_genre.fetch(genre_id)
        # for result in top_genre.results:
        #     print(result.title)
        top_genre_id = [top_genre.results , data['name']]
        top_genre_collection.append(top_genre_id)
    # print(top_genre_collection)
    return templates.TemplateResponse(request=request , name='index.html',context={"top_year": top_year.results,"year" : year,"top_genre" :top_genre_collection} )

@app.post('/' , response_class=HTMLResponse)
def index_search(request: Request , search: str = Form(...)):
        search  = request.form["search"]
        # print(search)
        movie_dic = movie_collection()
        movie_dic.results=[]
        id_url = f"http://api.themoviedb.org/3/search/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&query={search}"
        movie_dic.fetch(id_url)
        return templates.TemplateResponse(request=request, name='landing.html',context={"movie":movie_dic.results, "key_word":search})

# @app.route('/details/<id>')
# def details(id):
#     url = f"http://api.themoviedb.org/3/movie/{id}?api_key=da396cb4a1c47c5b912fda20fd3a3336"
#     data = json.loads(requests.get(url).text)
#     data_json = movie(data["id"],data["title"],data["poster_path"],data["vote_average"],data["release_date"],data["overview"],data["backdrop_path"])
#     return render_template('details.html', movie=data_json)

# @app.route('/recommand', methods=['GET', 'POST'])
# def recommand():
#     if request.method == 'GET':
#         return render_template('recommand.html')
    
#     elif request.method =='POST':
#         m_name = request.form['movie_name']
#         m_name = m_name.title()
#         if m_name not in all_titles:
#              id_url = f"http://api.themoviedb.org/3/search/movie?api_key=da396cb4a1c47c5b912fda20fd3a3336&query={m_name}"
#              data = json.loads(requests.get(id_url).text)['results']
#              name_list=[i['original_title'] for i in data]
             
#              return render_template('negative.html' , name_list =name_list , name=m_name )
#         else:
#             vectorizer = RECOMMAND(TfidfVectorizer)
#             result_df = vectorizer.get_recommandation(m_name)
#             data=[]
#             # print(list(result_df['title']))
#             for i in range(len(result_df)):
#                 data.append((list(result_df["title"])[i] , list(result_df["date"])[i]))
#             print(data)
#             return render_template('positive.html', movie_data= data , search_name=m_name)
        # print(name_list)    
        # return name_list
  
