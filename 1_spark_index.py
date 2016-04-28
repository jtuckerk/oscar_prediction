from pyspark import SparkConf, SparkContext

import sys
import re

from variables import MACHINE, VUID, PAGE_TABLE, INDEX_TABLE, COLUMN_FAMILY, COLUMN

index_file = 'hdfs:///user/%s/word_index' % VUID

 
'''
A good example can be found at: http://www.mccarroll.net/blog/pyspark2/
'''
def index(spark, wiki_file):
    wiki_data = spark.textFile(wiki_file)

def get_title_and_text(text):
    return (get_title(text), get_text(text))


def get_title(text):
    title = '<title>'
    title_end = '</title>'
    start = text.index(title) + len(title)
    end = text.index(title_end)
    return text[start:end].lower()


def get_text(text):
    text_tag = '<text xml:space="preserve">'
    text_end = '</text>'
    start = text.index(text_tag) + len(text_tag)
    end = text.index(text_end)
    text_block = text[start:end].lower()
    return re.sub(r"\W+", ' ', text_block).strip().split(' ')[:MAX_WORDS]


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


