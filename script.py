import requests
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('api_key', type=str)
args = parser.parse_args()
api_key = args.api_key

current_page = 1
movies_count = 0
movies_id_list = []
movies_id_set = set()
similar_movies_pairs = []

while movies_count < 300:
    response = requests.get("https://api.themoviedb.org/3/discover/movie?api_key=" + api_key + "&sort_by=popularity.desc&page=" + str(current_page) + "&primary_release_date.gte=2000&with_genres=35")
    response_json = response.json()
    results_list = response_json["results"] 
    current_page += 1
    
    
    with open('movie_ID_name.csv', 'a') as csvfile:
        movies_csv = csv.writer(csvfile, delimiter=',')
        for movie in results_list:
            if movies_count == 300:
                break
            else:
                movies_csv.writerow([movie['id'],movie['title']])
                movies_id_list.append(movie['id'])
                movies_count += 1


for movie_id in movies_id_list:
    movies_id_set.add(movie_id)
    response = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) + "/similar?api_key=" + api_key)
    response_json = response.json()
    results_list = response_json["results"]

    similar_movies_count = 0
    while (similar_movies_count < 5 and similar_movies_count < len(results_list)):
        if results_list[similar_movies_count]["id"] not in movies_id_set:
            similar_movies_pairs.append([movie_id,results_list[similar_movies_count]["id"]])
        similar_movies_count += 1
        
with open('movie_ID_sim_movie_ID.csv', 'w') as csvfile:
    movies_csv = csv.writer(csvfile, delimiter=',')
    for pair in similar_movies_pairs: 
        movies_csv.writerow(pair)




    





