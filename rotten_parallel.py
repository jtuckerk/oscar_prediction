import omdb
import csv
import re

myfile = open("myfile", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL) 

with open('movies.list', 'r') as f:
    lines = []
    for line in f: 
        if line[0] == '"':
            line = line.strip()
            movtitle = re.search('"(.*)"', line)
            movtitle = movtitle.group(1)
            movyear = line[line.find("(")+1:line.find(")")]
            try: 
                movyear = int(movyear)
            except ValueError: 
                movyear = 0
            lines.append((str(movtitle), int(movyear)))
    #lines = set(lines)
'''
with open('testf', 'w') as f2:
    for item in lines: 
        f2.write("%s\n" % item)
'''
mlist = lines[:6000] #[('True Grit', 1969), ('True Grit', 2000), ('True Grit', 2010)]
scorelist = [] 
#print mlist
#movie = omdb.get(title='True Grit', year=1900, tomatoes=True)
#print movie

for item in mlist:
    movie = omdb.get(title=item[0], year=item[1], tomatoes=True)
    if str(movie) != "Item({})":
        mtitle = movie.title
        myear = movie.year
        critscore = movie.tomato_meter
        conscore = movie.tomato_user_meter
        mid = movie.imdb_id
        if str(critscore) != "N/A":
            scorelist.append(mid + ", " + mtitle + ", " + myear + ", " + critscore + ", " + conscore)
            print("working")
wr.writerow(scorelist)
