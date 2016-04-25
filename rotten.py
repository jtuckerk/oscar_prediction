import omdb
import csv
import re

myfile = open("myfile", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL) 
'''
with open("movies.list") as f: 
    movielist = list(csv.reader(f))
test = open("testf", 'wb')
writ = csv.writer(test, quoting=csv.QUOTE_ALL)
writ.writerow(movielist)
'''

with open('movies.list', 'r') as f:
    #lines = f.read().splitlines()
    lines = []
    for line in f: 
        if line[0] == '"':
            line = line.rstrip('\n')
            movtitle = re.search('"(.*)"', line)
            movtitle = movtitle.group(1)
            movyear = line[line.find("(")+1:line.find(")")]
            lines.append("'" + movtitle + "', " + movyear)

with open('testf', 'w') as f2:
    for item in lines: 
        f2.write("%s\n" % item)

mlist = [('True Grit', 1969), ('True Grit', 2010)]
scorelist = [] 

#movie = omdb.get(title='True Grit', year=1969, tomatoes=True)
for item in mlist:
    movie = omdb.get(title=item[0], year=item[1], tomatoes=True)
    mtitle = movie.title
    myear = movie.year
    critscore = movie.tomato_meter
    conscore = movie.tomato_user_meter
    mid = movie.imdb_id

    print("(" + mid + ", " + mtitle + ", " + myear + ", " + critscore + ", " + conscore + ")")
    scorelist.append(("(" + mid + ", " + mtitle + ", " + myear + ", " + critscore + ", " + conscore + "\
)"))

wr.writerow(scorelist)
