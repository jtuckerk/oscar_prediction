from pyspark import SparkConf, SparkContext

import sys
import sys
sys.path.insert(0, "/home/kirvenjt/.conda/envs/venv/lib/python2.7/site-packages")

from DB import DB
DB_NAME = 'imdb'
db = DB(DB_NAME)
import omdb
import csv
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

index_file = 'hdfs:///user/%s/word_index' % VUID
test_file = 'hdfs:///user/kirvenjt/oscar_data/testout'
'''
Doesn't work cannot import something from DB
'''
def index(spark, wiki_file):
    wiki_data = spark.textFile(wiki_file)
#use this for testing after map
#.take(300)
#             .flatMap(lambda x: [(x[0], x[1], x[2], x[3], x[4]) for x in x])\
#             .map(api_request)\
#             .filter(no_review)\

    c = wiki_data.map(get_title_and_year)\
             .filter(has_name_and_year)\
             .map(test_db_query)\
             .saveAsTextFile(test_file)
    #open("count.txt", 'w').write(str(c))

def test_db_query(title_year):
    t = title_year[0] 
    y = title_year[1]
    q = "SELECT * FROM movies WHERE title="+t+" AND year="+y
    return db.query(q)
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
    conf.set("spark.executor.memory", "1g")
    conf.set("spark.driver.memory", "1g")
    conf.set("spark.executor.memory", "1g")
    conf.set("spark.executor.instances","100")
    conf.set("spark.executor.cores","100")
    conf.set("spark.cores.max", "10")


    spark = SparkContext(conf = conf)
    index(spark, sys.argv[2])


