from pyspark import SparkConf, SparkContext

import sys

import omdb
import csv
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

all_movies = 'hdfs:///user/kirvenjt/oscar_data/omdb_responses'
test = 'hdfs:///user/kirvenjt/oscar_data/test'
imdb_file = 'hdfs:///user/kirvenjt/oscar_data/top10ActorsPerMovie.txt'

    #                     .saveAsTextFile(test)\

'''
an attempt at doing the rotten api requests from spark - too slow
'''
def create_y(spark):
    imdb_data = spark.textFile(imdb_file)
    movie_data = spark.textFile(all_movies)

    imdb_data = imdb_data.map(get_imdb_fields)\
                         .filter(has_name_and_year)\
                         .keyBy(lambda x: (x[0], get_int_clean(x[1])))\
 #                        .map(lambda (x,y): (x,y,1))\

    movie_data = movie_data.map(get_fields)\
                           .filter(has_name_and_year)\
                           .map(lambda x: (x[1], x[2]))\
                           .keyBy(lambda x: (x[0], get_int_clean(x[1])))\

    c = movie_data.join(imdb_data).count()
    print c
'''
    movie_data = movie_data.map(get_fields)\
                           .map(lambda x: (x[1], x[2]))\
                           .keyBy(lambda x: (x[0], get_int_clean(x[1])))\

           

    movie_data.leftOuterJoin(oscar_data)\
              .map(lambda x: (x[0],encoding(x[1])))\
              .distinct()\
              .reduceByKey(lambda x,y: x+y)\
              .saveAsTextFile(test)
'''
def has_name_and_year(title_year):
    return not (title_year[0] == "" or title_year[1]=="")

def encoding(item):
    if not item[1]:
        return 0
    if item[1][1] in movie_awards:
        return 2
    else:
        assert item[1][1] in actor_awards
        return 1

def get_int_clean(item):
    return int(re.findall(r'\d{4}', item).pop())
def p(item):
    print item

def get_fields(text):
    return eval(text)

def get_imdb_fields(text):
    text = text.split('|')
    a = [x.strip() for x in text]
    return a

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
    create_y(spark)
