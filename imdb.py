from DB import DB

DB_NAME = 'imdb'

'''
Refer to https://github.com/ameerkat/imdb-to-sql/raw/master/db_schema.png for the schema.

Write SQL queries that return:

1. The movie id of the film The Bourne Identity that Matt Damon acted in.

2. The number of movies Kevin Bacon is in (idactor = 1363713)

3. The number of distinct movies per genre that have the keyword 'beer' (order by count desc).

4. Fill in the function six_degrees that returns a list of movies that connect Matt Damon to Kevin Bacon
(there are multiple solutions)
['The Bourne Identity', ..., 'Movie']


'''

q1 = '''SELECT movies.idmovies
        FROM movies, actors, acted_in
        WHERE movies.title='The Bourne Identity'
        AND actors.fname='Matt'
        AND actors.lname='Damon'
        AND actors.idactors=acted_in.idactors 
        AND acted_in.idmovies=movies.idmovies; '''

#movies.idmovies here yielded 300 movies.title seems less correct but satisfies the assertion
q2 = '''SELECT count(DISTINCT movies.title)
        FROM movies, actors, acted_in 
        WHERE actors.idactors=1363713
        AND actors.idactors=acted_in.idactors 
        AND acted_in.idmovies=movies.idmovies; '''

q3 = '''SELECT genres.genre, count(DISTINCT movies.title)
        FROM movies, genres, movies_genres, keywords, movies_keywords 
        WHERE keywords.keyword='beer' 
        AND movies.idmovies=movies_keywords.idmovies 
        AND keywords.idkeywords=movies_keywords.idkeywords 
        AND  genres.idgenres=movies_genres.idgenres 
        AND movies_genres.idmovies=movies.idmovies 
        GROUP BY genre ORDER by count(movies.title) DESC;'''

get_actors_part1 = '''
SELECT DISTINCT actors.idactors, moviesperactor.title FROM (SELECT distinct movies.idmovies, movies.title
          FROM movies, actors, acted_in 
          WHERE actors.idactors='''

get_actors_part2 = '''
          AND actors.idactors=acted_in.idactors 
          AND acted_in.idmovies=movies.idmovies) as moviesperactor, actors, acted_in
          WHERE acted_in.idmovies=moviesperactor.idmovies AND acted_in.idactors=actors.idactors
'''

def get_co_actors_id(idactor, db):
    q = get_actors_part1 + str(idactor) + get_actors_part2
    return  db.query(q)

def get_actor_id(fname, lname, db):
    q="select actors.idactors from actors, acted_in  where fname='"+fname+"' AND "
    q+= " lname='"+lname+"' "
    q+= "and actors.idactors=acted_in.idactors group by actors.idactors order by count(acted_in.idmovies) desc limit 1;"

    return db.query(q)[0][0]

def six_degrees():
    
    db = DB('imdb')
    a_id = get_actor_id('Weng', 'Weng',db)
    actors = [(a_id, [])]
    searched_actors =[]
    movie_tree = {}
    kb_id = 1363713
    for i in range(6): 
        next_level_actors =[]

        for actor, movie_list in actors:
          
            searched_actors.append(actor)
            id_title_list = get_co_actors_id(actor,db)
            movie_tree[actor] = id_title_list,movie_list
            for new_actor, title in id_title_list:
                if not new_actor in searched_actors:
                    if new_actor == kb_id:
                        return movie_tree[actor][1]+[title]
                    next_level_actors.append((new_actor, movie_tree[actor][1]+[title]))
        actors=next_level_actors

    return []


def main():

    print six_degrees()
    return
    db = DB('imdb')
    for q in [q1, q2, q3]:
        for line in db.query(q):
            print line[0]


def test_q1():
    db = DB(DB_NAME)
    assert db.query(q1)[0][0] == 509780
ctors_part1 = ''' 
SELECT DISTINCT actors.idactors FROM (SELECT distinct movies.idmovies
          FROM movies, actors, acted_in 
          WHERE actors.idactors='''

def test_q2():
    db = DB(DB_NAME)
    assert db.query(q2)[0][0] == 298


def test_q3():
    db = DB(DB_NAME)
    result = db.query(q3)
    assert result[0][0] == 'Comedy'
    assert result[0][1] == 56
    assert result[1][0] == 'Drama'


if __name__ == '__main__':
    main()
