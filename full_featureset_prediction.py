# conda install scikit-learn
import scipy
import numpy as np
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold
from sklearn import svm
import codecs
import re
#from sklearn.neural_network import MLPClassifier

def load():
    return load_batting(), load_allstars()

#loads (tite,year) with [,0,0,0,] plot representation
def get_input():

    OMDB = True
    IMDB_experience = True
    IMDB_oscar_prior = True 
    PLOT = False #better or the same without this

    #adding 6 features: scores from rotten tomoatoes, metacritic, and IMDB
    # as well as the movie duration
    ombd_file = './data/omdb_data.txt'
    omdb_feats = {}
    print "Getting OMDB features"
    with codecs.open(ombd_file, 'r', encoding='utf-8') as r:
        for l in r.readlines():
            l=eval(l)
            assert len(l) == 14

            critic_score = float(l[3])
            audiance_score = float(l[4]) if l[4] != 'N/A' else 0
            duration = float(l[6].split()[0]) if l[6] != 'N/A' else 0
            metascore = float(l[7]) if l[7] != 'N/A' else 0
            imdb_rating = float(l[10].replace(",", '')) if l[10] != 'N/A' else 0
            imdb_votes =  float(l[11].replace(",", '')) if l[11] != 'N/A' else 0
            #year = int(re.findall(r'\d{4}', l[2]).pop())

            features = [critic_score, audiance_score, duration, metascore, imdb_rating, imdb_votes]
            title_year = (l[1], re.findall(r'\d{4}', l[2]).pop())
            omdb_feats[title_year] = features


    #adding 10 features: prior oscar nomination counts for the actors in the top 10
    # billing positions
    actor_oscar_info = './data/actor_oscar_prior.txt'
    actor_oscar_feats = {}
    actor_oscar_size = 10
    print "Getting IMDB actor related features"
    with codecs.open(actor_oscar_info, 'r', encoding='utf-8') as r:
        for l in r.readlines():
            l=eval(l)
            assert len(l[1]) == 10

            actor_oscar_feats[l[0]] = l[1]#+[l[0][1]])

    #adding 10 features: prior movies acted in counts for the actors in the top 10
    # billing positions
    actor_experience_data = './data/actor_experience.txt'
    actor_ex_feats = {}
    actor_ex_size = 10
    with codecs.open(actor_experience_data, 'r', encoding='utf-8') as r:
        for l in r.readlines():
            l=eval(l)
            assert len(l[1]) == 10
            actor_ex_feats[l[0]] = l[1]

    #adding 128 features: a plot summary represented as a vector
    #  created as the average of the non stopword word embedding
    #  vectors from the plot for each movie
    plot_embedding_data = './data/plot_embeddings.txt'
    plot_embedding_feats = {}
    plot_embedding_size = 128
    print "Getting plot vector representations"
    with codecs.open(plot_embedding_data, 'r', encoding='utf-8') as r:
        for l in r.readlines():
            l=eval(l)
            assert len(l[1]) == plot_embedding_size
            plot_embedding_feats[l[0]] = l[1]

    feats = {}
    # fill any missing features with all 0's and combine features to single array
    a,b,c,d = [],[],[],[]
    for k in omdb_feats.keys():
        if OMDB:
            a = omdb_feats[k]
        if IMDB_experience:
            b = actor_ex_feats[k] if k in  actor_ex_feats else [0]*actor_ex_size
        if IMDB_oscar_prior:
            c = actor_oscar_feats[k] if k in  actor_oscar_feats else [0]*actor_oscar_size
        if PLOT:
            d = plot_embedding_feats[k] if k in  plot_embedding_feats else [0]*plot_embedding_size       
        feats[k] = np.array(a+b+c+d)
    return feats

def determine_y(encoding):
    #0 no wins 
    #1 actor win/nom
    #2 movie win/nom
    #3 actor+movie win

    if encoding <1:
        return 0
    else:

        return 1
def get_output():
    oscars = {}
    oscar_file = './oscar_y/oscar_y_full'
    with codecs.open(oscar_file, 'r', encoding='utf-8') as r:
        for l in r.readlines():
            l=eval(l)
            y = determine_y(l[1])
            #leave out any non winners - if missing in dict assume not winner 
            if y:
                oscars[(l[0][0], unicode(l[0][1]))] =y 
    return oscars

def get_X_y(input_dict, output_dict):
    X = []
    y = []
    #make sure we have an input for all oscar winners or noms
    #for k in output_dict.keys():
    #    assert k in input_dict

    for k in input_dict.keys():
        X.append(input_dict.get(k, np.zeros(20)))
        y.append(output_dict.get(k, 0))

    return np.array(X), np.array(y)
def test_classifier(clf, X, Y):
    folds = StratifiedKFold(Y, 5)
    aucs = []
    count =0
    for train, test in folds:
        # Sizes
        # print X[train].shape, Y[train].shape
        # print X[test].shape, len(prediction)

        clf.fit(X[train], Y[train])
        prediction = clf.predict_proba(X[test])
        aucs.append(roc_auc_score(Y[test], prediction[:, 1]))
        count +=1
        if count >=1:
            #break
            pass
        
    print clf.__class__.__name__, aucs, np.mean(aucs)

import time
def main():
    X, Y = get_X_y(get_input(), get_output())

    clf = linear_model.SGDClassifier(loss='log')
    test_classifier(clf, X, Y)

    clf = GaussianNB()
    test_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    test_classifier(clf, X, Y)

if __name__ == '__main__':
    main()
