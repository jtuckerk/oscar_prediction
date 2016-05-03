from gensim import models
from nltk.corpus import stopwords
import codecs
import numpy as np
import re

stop = stopwords.words('english')
stop = set(stop)

print "loading w2v model"
m = models.Word2Vec.load_word2vec_format('/Users/tuckerkirven/Desktop/w2v_model.w7s128.bin', binary=True)
print m
def replace_punc(line):

    puncs = ['.',',','','!','?',')','(','"',"'",':', ';', '/', ']','[']
    for p in puncs:
        line = line.replace(p, ' ')

    return line

with codecs.open('./plot_responses.txt', 'r', encoding='utf-8') as r, codecs.open('plot_embeddings.txt', 'w', encoding='utf-8') as w_file:
    for line in r.readlines():
        vals = line.split(" ||| ")
        title = vals[1].strip()
        year = int(re.findall(r'\d{4}', vals[2]).pop())
        line = replace_punc(line)
        vecs = []
        for w in line.split():
            w = w.lower().strip()
            
            if w not in stop:
                try:
                    vecs.append(m[w])
                except Exception as e:
                    #oh well word not in model
                    pass

        if len(vecs) ==0:
            avg_vecs = np.zeroes(128)
        else: 
            vecs = np.array(vecs)
            avg_vec = np.average(vecs, axis=0 )

        vec_list = avg_vec.tolist()

        w_file.write(str(((title,year),vec_list))+'\n')
