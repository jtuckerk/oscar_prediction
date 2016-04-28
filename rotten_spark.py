from pyspark import SparkConf, SparkContext

import sys

import omdb
import csv
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

index_file = 'hdfs:///user/%s/word_index' % VUID
test_file = 'hdfs:///user/kirvenjt/testfile'
'''
A good example can be found at: http://www.mccarroll.net/blog/pyspark2/
'''
def index(spark, wiki_file):
    wiki_data = spark.textFile(wiki_file)
#use this for testing after map
#.take(300)
#             .flatMap(lambda x: [(x[0], x[1], x[2], x[3], x[4]) for x in x])\
    wiki_data.map(get_title_and_year)\
             .filter(has_name_and_year)\
             .map(api_request)\
             .filter(no_review)\
             .saveAsTextFile(test_file)

def no_review(item):
    return item != None
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
    return len(title_year)==2 and not (title_year[0] == "" or title_year[1]=="")

def get_title_and_year(text):
    t = text.split("|")
    t = t[1:] # leave off id
    return [x.strip() for x in t]

if __name__ == '__main__':
    conf = SparkConf()
    if sys.argv[1] == 'local':
        conf.setMaster("local[3]")
        print 'Running locally'
    elif sys.argv[1] == 'cluster':
        conf.setMaster("spark://10.0.22.241:7077")
        print 'Running on cluster' 
    conf.set("spark.executor.memory", "10g")
    conf.set("spark.driver.memory", "10g")
    spark = SparkContext(conf = conf)
    index(spark, sys.argv[2])


