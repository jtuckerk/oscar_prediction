import omdb
import csv

myfile = open("myfile", 'wb')
wr = csv.writer(myfile, quoting=csv.QUOTE_ALL) 

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
