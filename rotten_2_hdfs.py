from pyspark import SparkConf, SparkContext

import sys

import csv
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

test_file = 'hdfs:///user/kirvenjt/oscar_data/testout'
'''
Simply moving from the rotten api request output into a title, year file
'''
def move(spark, rotten_file):
    rotten_data = spark.textFile(rotten_file)

    c = rotten_data.map(get_title_and_year)\
             .filter(has_name_and_year)\
             .saveAsTextFile(test_file)
    #open("count.txt", 'w').write(str(c))


def has_name_and_year(title_year):
    return len(title_year)==2 and not (title_year[0] == "" or title_year[1]=="")

def get_title_and_year(text):
    t = text.split(" ||| ")
    t = t[1:3] # leave off id
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
    move(spark, sys.argv[2])


