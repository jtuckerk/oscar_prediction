from pyspark import SparkConf, SparkContext

import sys

import omdb
import csv
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

all_movies = 'hdfs:///user/kirvenjt/oscar_data/omdb_responses'
test = 'hdfs:///user/kirvenjt/oscar_data/actor_experience'
imdb_file = 'hdfs:///user/kirvenjt/oscar_data/top10ActorsPerMovie.txt'

    #                     .saveAsTextFile(test)\

'''
an attempt at doing the rotten api requests from spark - too slow
'''
def create_y(spark):
    imdb_data = spark.textFile(imdb_file)
    movie_data = spark.textFile(all_movies)
    
#            
    imdb_data = imdb_data.map(get_imdb_fields)\
                         .filter(lambda x: wrong_field_size(x, 5))\
                         .keyBy(lambda x: (x[0], get_int_clean(x[1])))


    movie_data = movie_data.map(get_fields)\
                           .filter(lambda x: has_name_and_year(x[1], x[2]))\
                           .map(lambda x: (x[1], x[2]))\
                           .keyBy(lambda x: (x[0], get_int_clean(x[1])))\
#((u'Brush with Danger', 2014), ((u'Brush with Danger', u'2014'), [u'Brush with Danger', u'2014', u'Stephanie', u'Hilbert', u'6']))
    movie_data.join(imdb_data)\
              .map(lambda (key, (key2,info)): tuple(info))\
              .distinct()\
              .saveAsTextFile(test)


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
def wrong_field_size(item, size):
    return len(item) == size
def has_name_and_year(title, year):
    return not (title == "" or len(year)!=4)

def encoding(item):
    if not item[1]:
        return 0
    if item[1][1] in movie_awards:
        return 2
    else:
        assert item[1][1] in actor_awards
        return 1
def filter_broken_year(year):
    try:
        int(re.findall(r'\d{4}', item).pop())
    except Exception as e:
        return False

    return True
def get_int_clean(item):
    try:
        year =  int(re.findall(r'\d{4}', item).pop())
    except Exception as e:
        return 0

    return year

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
