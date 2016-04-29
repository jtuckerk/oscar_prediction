import omdb
import csv
import re
import codecs
outfile = codecs.open("responses.txt", 'w', encoding='utf-8')


    #lines = set(lines)
'''
with open('testf', 'w') as f2:
    for item in lines: 
        f2.write("%s\n" % item)
'''
 #[('True Grit', 1969), ('True Grit', 2000), ('True Grit', 2010)]
scorelist = [] 
#print mlist
#movie = omdb.get(title='True Grit', year=1900, tomatoes=True)
#print movie
import  multiprocessing
print "seems legit"


def request(item):

    try:
        movie = omdb.get(title=item[0], year=item[1], tomatoes=True)
    except Exception as e:
        print e, "caused by", item[0]
        return None
    if str(movie) != "Item({})":
        mtitle = movie.title
        myear = movie.year
        critscore = movie.tomato_meter
        conscore = movie.tomato_user_meter
        mid = movie.imdb_id
        med_type =movie.type
        runtime = movie.runtime
        metascore= movie.metascore
        lang = movie.language
        released = movie.released
        imdb_rating = movie.imdb_rating
        imdb_votes = movie.imdb_votes
        box_office = movie.box_office
        country = movie.country


        if str(critscore) != "N/A":
            return mid + " ||| " + mtitle + " |||  " + myear + " |||  " + critscore + " |||  " + conscore + mid + " ||| " + med_type + " ||| " + runtime + " ||| " + metascore + " ||| " + lang + " ||| " + released + " ||| " + imdb_rating + " ||| " + imdb_votes + " ||| " + box_office + " ||| " + country + " ||| " + "\n"
        else:
            return None
 
p = multiprocessing.Pool(10)
import sys
def get_movies():
    with codecs.open('./movies.list.clean/list0-299999.txt', 'r', encoding='utf-8') as f:
        lines = []
        for line in f.readlines(): 

           line = line.strip()
           l = eval(line)

           movtitle = l[0]
           movyear = l[1]
           try: 
               movyear = int(movyear)
           except ValueError: 
               movyear = 0
           yield (unicode(movtitle), int(movyear))

count =0
import time
start = time.time()
for result in p.imap(request, get_movies()):
    # (filename, count) tuples from worker                                                                                                                                         
    count +=1
    if result:
        outfile.write(result)
    if count%500==0:
        print count, int((time.time()-start))
        sys.stdout.flush()
