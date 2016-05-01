From pyspark import SparkConf, SparkContext

import sys

import omdb
import csv
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

index_file = 'hdfs:///user/%s/word_index' % VUID
test_file = 'hdfs:///user/kirvenjt/oscar_data/omdb_responses'
'''
an attempt at doing the rotten api requests from spark - too slow
'''
def index(spark, wiki_file):
    wiki_data = spark.textFile(wiki_file)
#use this for testing after map

#             .flatMap(lambda x: [(x[0], x[1], x[2], x[3], x[4]) for x in x])\
#             .map(api_request)\
#             .filter(no_review)\

    c = wiki_data.map(get_fields)\
             .filter(has_name_and_year)\
             .saveAsTextFile(test_file)
    #open("count.txt", 'w').write(str(c))

def no_review(item):
    return item != None
awards = ['Best Picture',
          'Best Actor in a Supporting Role',
          'Best Actor in a Leading Role',
          'Best Performance by an Actor in a Leading Role',
          'Best Writing, Screenplay',
          'Best Actress in a Leading Role',
          'Best Actress in a Supporting Role',
          'Best Director',
          'Best Writing, Motion Picture Story',
          'Best Actress in a Supporting Role',
          'Best Motion Picture of the Year',
          'Best Writing, Original Story']
def awards_we_want(item):
    return item[1] in awards 

def api_request(item):
    movie = omdb.get(title=item[0], year=item[1], tomatoes=True)
    if str(movie) != "Item({})":
        mtitle = movie.title
        myear = movie.year
        critscore = movie.tomato_meter
        conscore = movie.tomato_user_meter
        mid = movie.imdb_id
        if str(critscore) != "N/A":
            return (mid, mtitle, myear, critscore, conscore)
        else:
            return None
def has_name_and_year(title_year):
    return not (title_year[0] == "" or title_year[1]=="")

def get_fields(text):
    t = text.split(" ||| ")
    t[4] = t[4].replace(t[0], '')
    return [x.strip() for x in t[:-1]]

if __name__ == '__main__':
    conf = SparkConf()
    if sys.argv[1] == 'local':
        conf.setMaster("local[3]")
        print 'Running locally'
    elif sys.argv[1] == 'cluster':
        conf.setMaster("spark://10.0.22.241:7077")
        print 'Running on cluster' 
    conf.set("spark.executor.memory", "1g")
    conf.set("spark.driver.memory", "1g")
    conf.set("spark.executor.memory", "1g")
    conf.set("spark.executor.instances","100")
    conf.set("spark.executor.cores","100")
    conf.set("spark.cores.max", "10")


    spark = SparkContext(conf = conf)
    index(spark, sys.argv[2])


