from pyspark import SparkConf, SparkContext

import sys

import omdb
import csv
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

oscar_file = 'hdfs:///user/kirvenjt/oscar_data/oscar_winners_clean'
all_movies = 'hdfs:///user/kirvenjt/oscar_data/omdb_responses'
oscar_y = 'hdfs:///user/kirvenjt/oscar_data/oscar_y'

'''
an attempt at doing the rotten api requests from spark - too slow
'''
def create_y(spark):
    oscar_data = spark.textFile(oscar_file)
    movie_data = spark.textFile(all_movies)
#                           .keyBy(lambda x: (x[2], get_int_clean(x[0])-1))\     
    oscar_data = oscar_data.map(get_fields)\
                           .keyBy(lambda x: (x[2], get_int_clean(x[0])-1))\


    movie_data = movie_data.map(get_fields)\
                           .map(lambda x: (x[1], x[2]))\
                           .keyBy(lambda x: (x[0], get_int_clean(x[1])))\

           

    movie_data.leftOuterJoin(oscar_data)\
              .map(lambda x: (x[0],encoding(x[1])))\
              .distinct()\
              .reduceByKey(lambda x,y: x+y)\
              .saveAsTextFile(oscar_y)

movie_awards = ['Best Picture',
                'Best Writing, Screenplay',
                'Best Director',
                'Best Writing, Motion Picture Story',
                'Best Motion Picture of the Year',
                'Best Writing, Original Story']

actor_awards = ['Best Actor in a Supporting Role',
                'Best Actor in a Leading Role',
                'Best Performance by an Actor in a Leading Role',
                'Best Actress in a Leading Role',
                'Best Actress in a Supporting Role',]
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


    ((fname, lname), (original))
