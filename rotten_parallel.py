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

    movie = omdb.get(title=item[0], year=item[1], tomatoes=True)
    if str(movie) != "Item({})":
        mtitle = movie.title
        myear = movie.year
        critscore = movie.tomato_meter
        conscore = movie.tomato_user_meter
        mid = movie.imdb_id
        if str(critscore) != "N/A":
            return mid + " ||| " + mtitle + " |||  " + myear + " |||  " + critscore + " |||  " + conscore + "\n"
        else:
            return None
 
p = multiprocessing.Pool(32)

def get_movies():
    with codecs.open('./movies.list.clean/list.txt', 'r', encoding='utf-8') as f:
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
for result in p.imap(request, get_movies()):
    # (filename, count) tuples from worker
    count +=1
    if result:
        outfile.write(result)
    if count%5000==0:
        print count

