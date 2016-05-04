import omdb
import csv
import re
import codecs

outfile = codecs.open("plot_responses.txt", 'w', encoding='utf-8')


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
        movie = omdb.get(title=item[0], year=item[1], tomatoes=True, fullplot=True)
    except Exception as e:
        print e, "caused by", item[0]
        return None
    if str(movie) != "Item({})":
        mtitle = movie.title
        myear = movie.year
        plot = movie.plot
        mid = movie.imdb_id
        plot = plot.replace('\n', ' ')
        if True:
            return mid + " ||| " + mtitle + " |||  " + myear + " |||  " + plot
        else:
            return None
 
p = multiprocessing.Pool(32)
import sys
def get_movies():
    with codecs.open('./movies.list.short/full', 'r', encoding='utf-8') as f:
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
           yield unicode(movtitle), int(movyear)

count =0
import time
import collections
year_data= collections.defaultdict(int)
for title, year in get_movies():
    year_data[year] += 1

for y, count in sorted(year_data.items()):
    print y, count
