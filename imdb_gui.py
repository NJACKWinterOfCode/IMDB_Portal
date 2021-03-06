import requests
import os
import sys
import json
import bs4

if sys.version[0] == '3':
    raw_input = input

os.system('clear')


status = open('info.txt','a')



def info_movie(name):
    try:
        movie_name = name.replace(' ','%20')
        movie_url = 'https://api.themoviedb.org/3/search/movie?' \
                    'api_key=ffb07b773769d55c36ccd83845385205&language=en-US&query='\
                    + str(movie_name) + '&page=1&include_adult=false'
        response = requests.get(movie_url)
        results_json = json.loads(response.text)
        results  = results_json['results']
        movie_id = results[0]['id']
        movie_id_url = 'https://api.themoviedb.org/3/movie/'+str(movie_id)\
                        + '?api_key=ffb07b773769d55c36ccd83845385205&language=en-US'
        response = requests.get(movie_id_url)
        movie_details = json.loads(response.text)

        movie_list = []

        movie_title = movie_details['title']
        movie_imdb_id = movie_details['imdb_id']
        movie_year = movie_details['release_date']
        movie_genre = movie_details['genres']
        movie_language = movie_details['spoken_languages']
        movie_duration = movie_details['runtime']
        movie_plot = movie_details['overview']

        imdb_id_url = 'http://www.imdb.com/title/'+str(movie_imdb_id)
        response = requests.get(imdb_id_url)
        html = response.text
        soup = bs4.BeautifulSoup(html,"lxml")
        data = soup.select('.ratingValue')
        movie_rating = data[0].get_text('',strip=True)
        
        if sys.version[0] != '3':
            movie_title = movie_title.encode('ascii', 'ignore')
            movie_rating = movie_rating.encode('ascii', 'ignore')
            movie_year = movie_year.encode('ascii', 'ignore')
            movie_plot = movie_plot.encode('ascii', 'ignore')
        movie_list = [movie_title, movie_rating, movie_year, str(movie_duration), movie_genre[0]['name'], movie_plot]
        status.write ("\n\n--------------------------------------MOVIE INFORMATION---------------------------------\n")
        status.write ("\n\t TITLE       : \t\t"+movie_title)
        status.write ("\n\t IMDB RATING : \t\t"+movie_rating)
        status.write ("\n\t RELEASED ON : \t\t"+movie_year)
        status.write ("\n\t DURATION    : \t\t"+str(movie_duration)+" mins")
        # status.write ("\n\t LANGUAGE    : \t\t"+language[0]['name'])
        status.write ("\n\t GENRE       : \t\t"+movie_genre[0]['name'])
        status.write ("\n\t PLOT        : \t\t"+movie_plot)

        return movie_list

    except KeyError:
        print ("\nNo such movie titled '"+name+"' found!\n")
        status.write ("\nNo such movie titled '"+name+"' found!\n")
    
    
def top_movies(rank):
    rank_url = 'http://www.imdb.com/chart/top'
    response = requests.get(rank_url)
    html = response.text
    soup = bs4.BeautifulSoup(html,"lxml")
    rows = soup.select('.lister-list tr')

    status.write ("\n"+"---------------------------TOP " + str(rank) + 
                  " MOVIES ACCORDING TO IMDB RATINGS-----------------------------"+"\n\n")
    status.write (" \t   TITLE\t\t\t\t\t\t\t\t\t\t   IMDB RATING\n\n")

    list_of_movies=[]

    for row in range(0,rank):
        movie_data=rows[row].select('td')
        movie_name=movie_data[1].get_text(' ',strip=True)
        movie_rating=movie_data[2].get_text(' ',strip=True)
        movie_details=("\n "+movie_name.ljust(75,' ')+"\t\t\t\t"+movie_rating+"\n")
        if sys.version[0] != '3':
            movie_details = movie_details.encode('ascii', 'ignore')
        movie_list=[movie_name, movie_rating]
        list_of_movies.append(movie_list)
        status.write (movie_details)
    
    return list_of_movies
        
        
def folder(path):
    dirs = os.listdir(path)
    status.write ('Showing results for the path: '+path+'\n')
    folder_list=[]
    for i in range(len(dirs)):
        dir_name = dirs[i]
        if dir_name == '.DS_Store':
            continue
        name = dir_name.replace(' ', '%20')
        movie_url = 'https://api.themoviedb.org/3/search/movie?' \
                    'api_key=ffb07b773769d55c36ccd83845385205&language=en-US&query='\
                    + str(name) + '&page=1&include_adult=false'
        response = requests.get(movie_url)
        results_json = json.loads(response.text)
        results = results_json['results']
        movie_id = results[0]['id']
        movie_id_url = 'https://api.themoviedb.org/3/movie/' + str(movie_id)\
                       + '?api_key=ffb07b773769d55c36ccd83845385205&language=en-US'
        response = requests.get(movie_id_url)
        movie_details = json.loads(response.text)

        try:
            movie_title = movie_details['title']
            movie_year = movie_details['release_date']
            movie_imdb_id = movie_details['imdb_id']

            imdb_id_url = 'http://www.imdb.com/title/' + str(movie_imdb_id)
            response = requests.get(imdb_id_url)
            html = response.text
            soup = bs4.BeautifulSoup(html, "lxml")
            data = soup.select('.ratingValue strong span')
            movie_rating = data[0].get_text('', strip=True)

            if sys.version[0] != '3':
                dir_name = dir_name.encode('ascii', 'ignore')
            folder_name = "[" + movie_rating + "] " + movie_title + " (" + movie_year[:4] + ")"
            if sys.version[0] != '3':
                folder_name = folder_name.encode('ascii', 'ignore')

            folder_list.append(folder_name)

            status.write("\n" + folder_name)
            os.rename(os.path.join(path, dir_name), os.path.join(path, folder_name))
            status.write('Renaming Done\n')
            
            return folder_list

        except KeyError:
            print("\nNo such movie titled '" + dir_name
                  + "' found or else read the instructions before using this feature!\n")
            status.write("\nNo such movie titled '" + dir_name
                         + "' found else read the instructions before using this feature!\n")
            
