# oscar_prediction
Big Data Project with Amy and Virinchi to predict which movies will be nominated for oscars

# This is more for notes for our team, for a cleaner explanation of our project see the report.

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
FILE: rotten_parallel.py - a parallelized version of rotten.py

Got plots from omdb
FILE: rot_par2: slightly different version of rotten_parallel

Created word embedding representations of the plots from omdb
Filtered out common words such as the, a, and...etc and punctuation
Using a word vector model created from a large amount of news and subtitle data,
get a word vector -- a numeric representation of the meaning more or less -- for 
each word in the plot summary. Average them all together to get a "plot" embedding
FILE: create_embeddings_from_plot.py

scraped oscar data directly from IMDB oscar page
FILE: scrape_oscar_data.py

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
FILE: oscar_y_create.py

used psql DB to get a list of all actors for all movies with billing number
FILE: Virinchi's query - not sure if in a file

Joined imdb actors for movie data with movies we "care" about as filtered based on whether or not they have Rotten tomatoes critic scores
FILE: actor_info_spark.py

Used this actor info to create actor experience and prior oscar win features for each
movie. ('The Revenant', 2015), [25, 12, 6...] would show that prior to this movie
the actor in billing position 1 had already acted in 25 movies. this same format was 
used for prior oscar nominations - wins and nominations are not distinguised.
FILE: get_actor_experience.py and get_actor_oscar_prior.py

Prediction files for the 3 different independent variables end in _prediction.py

All combined in full_featureset_prediction.py
The inclusion of certain features can be turned on or off with the boolean variables
in the get_input function near the top of the file

A few other spark files not explicitly described here were used for simply cleaning/filtering and loading into hdfs and joining sets of data.

Also tried doing omdb api requests from spark, but I think it overwhelmed their servers because it was very slow.
File: rotten_spark.py