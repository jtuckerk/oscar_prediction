from DB import DB
import codecs
import re
DB_NAME = 'imdb'

def get_title_year(line):
    l = eval(line)#should just return a tuple (title, year)
    #some years are 2004-2005 - just want first one
    year = re.search(r'(\d{4})', l[1]).group(0)
    return l[0], year 

def construct_query(title, year):

    q = "SELECT * FROM movies WHERE title="
    q+= "$$"+title +"$$ "
    q+= "AND "
    q+= "year ="
    q+= year
    return q

def main():
    db = DB(DB_NAME)
    with codecs.open("./movies.list.filter.clean", 'r', encoding='utf-8') as f, codecs.open("outfiletest.txt", 'w', encoding='utf-8')as outfile:
        for l in f.readlines():
            title, year = get_title_year(l)
            q = construct_query(title, year)
            result = db.query(q)
            if len(result) >3:
                print result
            outfile.write(str(result)+'\n')

if __name__ == '__main__':
    main()
