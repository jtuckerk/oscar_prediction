# oscar_prediction
Big Data Project with Amy and Virinchi to predict which movies will be nominated for oscars


Things done:

using 
$ psql -t -d imdb
> \o file.txt

> SELECT movies.idmovies, movies.title, movies.year
    FROM movies
    LEFT JOIN series
    ON moviesidmovies = series.idmovies
    WHERE series.idmovies IS NULL and not movies.type=1 and not movies.type=2;

to get all of the movies (no porn mostly no TV) to a text file
loaded to hdfs

From this list we got OMDB data which includes rotten tomato, imdb, and metacritic scores, as well as box office data such as release date and earnings we also used this to do an initial filtering of movies that are unlikely to win, we assumed if there is no critic score on rotten tomatoes it is not likely to win an oscar. From OMDB we also got rotten tomato movie descriptions which we plan to do word embedding analysis on. 

Cleaned omdb responses: hdfs:///user/kirvenjt/oscar_data/omdb_responses
 mid, mtitle, myear, critscore, conscore, media_type, runtime, metascore, lang, released, imdb_rating, imdb_votes, box_office, country

Oscar data uncleaned: 
hdfs:///user/kirvenjt/oscar_data/oscar_data.txt
includes 130ish awards going to be filtered and cleaned just to include specific awards
current format:
year ||| Award_title ||| Movie_title ||| Person ||| WON/LOSS

cleaned oscar data: hdfs:///user/kirvenjt/oscar_data/oscar_winners
in ['year', 'award_title',...] format with now only:
Best Picture
Best Actor in a Supporting Role
Best Actor in a Leading Role
Best Performance by an Actor in a Leading Role
Best Writing, Screenplay
Best Actress in a Leading Role
Best Actress in a Supporting Role
Best Director
Best Writing, Motion Picture Story
Best Actress in a Supporting Role
Best Motion Picture of the Year
Best Writing, Original Stor

oscar_y: in hdfs:///user/kirvenjt/oscar_data/oscar_y
for use in testing in format ((movie_title, year), win_code)
created with the file oscar_y_create which has an example joining.
win code is +1 for actor/actress nomination/win +2 for movie nomination/win
so a movie with a score of 3 has at least one actor win and movie, win which is any non actor related award from the list above 
we could make this file so we can test on wins vs nominations, but we dont have to