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

