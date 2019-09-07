import bs4
import re
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import time


# Create csv to write data to
filename = "imdb_data.csv"
f = open(filename, "w")
headers = "title,genre,director1,director2,actor1,actor2,actor3,actor4,box_office,imdb_rating,imdb_votes,yr,\n"
f.write(headers)

# Loop over
 # Years 
 # Numbers
# My selection criteria is: top 500 movies by # votes on IMDB over the year
years = range(1982, 2019)
num_movies = range(1, 500, 50)
for yr in years:
 for num in num_movies:
  # Get URL
  my_url = "https://www.imdb.com/search/title/?title_type=feature&year="+str(yr)+"-01-01,"+str(yr)+"-12-31&sort=num_votes,desc&start="+str(num)
  # Grab html from the URL
  uClient = uReq(my_url)
  # Read it
  page_html = uClient.read()
  # Close it
  uClient.close()
  # HTML parser
  page_soup = soup(page_html, "html.parser")
  # All the movie containers of interest
  movie_containers = page_soup.findAll("div", {"class": "lister-item-content"})
  # Exactly 50 movies based on this - will always be 50 movies 
  # Loop over movies
  for movie_index in range(len(movie_containers)):
   # Aim to get
   # imdb score + votes, genre, director(s), actor(s), box office
   container = movie_containers[movie_index]
   title = container.h3.a.text.replace(',', '')
      # Making rating into a number
   imdb_rating = container.div.div['data-value']
      # Genre requires cleaning
       # Some movies do not have genres so need to see if a genre, otherwise blank
   genre_container = container.p.findAll("span", {"class": "genre"})
   if (len(genre_container)>=1):
    genre = genre_container[0].text.strip().strip().replace(',','-')
   else:
    genre = '.'

   # Getting directors and actors
    # max # directors = 2
    # max # actors = 4
   # First get list of text of directors and actors
   directors_actors = container.findAll("p", {"class": ""})[1].text.replace('|',':').replace(',',':').replace('\n','').replace(' ', '').split(':')

   # Get director - use index 
   if ('Director' in directors_actors): 
    direct_index = directors_actors.index('Director')
    director1 = directors_actors[direct_index+1]
    # Store blank
    director2 = '.'
   elif ('Directors' in directors_actors):
    direct_index = directors_actors.index('Directors')
    director1 = directors_actors[direct_index+1]
    director2 = directors_actors[direct_index+2]

   # Get actors - use index; sometimes no stars in the summary
   if ('Stars' in directors_actors):
    act_index = directors_actors.index('Stars')
   else:
    act_index = len(directors_actors)

   total_act = len(directors_actors)-act_index

   if (total_act>=5):
    actor1 = directors_actors[act_index+1]
    actor2 = directors_actors[act_index+2]
    actor3 = directors_actors[act_index+3]
    actor4 = directors_actors[act_index+4]
   elif (total_act==4):
    actor1 = directors_actors[act_index+1]
    actor2 = directors_actors[act_index+2]
    actor3 = directors_actors[act_index+3]
    actor4 = '.'
   elif (total_act==3):
    actor1 = directors_actors[act_index+1]
    actor2 = directors_actors[act_index+2]
    actor3 = '.'
    actor4 = '.'
   elif (total_act==2):
    actor1 = directors_actors[act_index+1]
    actor2 = '.'
    actor3 = '.'
    actor4 = '.'
   else:
    actor1 = '.'
    actor2 = '.'
    actor3 = '.'
    actor4 = '.'


   # Get imdb votes and box office
    # Box office gross may not exist for all although seems like votes exists for all
   votes_box_office = container.findAll("p", {"class": "sort-num_votes-visible"})[0].findAll("span")
   imdb_votes = votes_box_office[1].get('data-value', None).replace(',', '')
   if len(votes_box_office)>3:
    box_office = votes_box_office[4].get('data-value', None).replace(',', '')
   else:
    box_office = '.'

   # Store in the CSV
   print('Title: ' + title)
   print('Genre: ' + genre)
   print('Director1: ' + director1)
   print('Director2: ' + director2)
   print('Actor1: ' + actor1)
   print('Actor2: ' + actor2)
   print('Actor3: ' + actor3)
   print('Actor4: ' + actor4)
   print('Box Office: ' + box_office)
   print('IMDB Rating: ' + imdb_rating)
   print('IMDB Votes: ' + imdb_votes)
   f.write(title + ',' + genre + ',' + director1 + ',' + director2 + ',' + actor1 + ',' + actor2 + ',' + actor3 + ',' + actor4 + ',' + box_office + ',' + imdb_rating + ',' + imdb_votes + ',' + str(yr) + '\n')
# Print year and movie number
  print(str(yr)+","+str(int((num-1)/50+1)))
# Wait 10 seconds before the next request/pull
  time.sleep(10)

# Close csv once done
f.close()
