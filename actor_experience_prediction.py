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
#from sklearn.neural_network import MLPClassifier

def load():
    return load_batting(), load_allstars()

#loads (tite,year) with [,0,0,0,] plot representation
def get_input():
    plots = {}
    plot_embedding_file = './plot_embeddings.txt'
    with codecs.open(plot_embedding_file, 'r', encoding='utf-8') as r:
        for l in r.readlines():
            l=eval(l)
            plots[l[0]] = np.array(l[1])#+[l[0][1]])
    return plots

def determine_y(encoding):
    #0 no wins 
    #1 actor win/nom
    #2 movie win/nom
    #3 actor+movie win

    if encoding !=2:
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
                oscars[l[0]] =y 
    return oscars

def get_X_y(input_dict, output_dict):
    X = []
    y = []
    #make sure we have an input for all oscar winners or noms
    for k in output_dict.keys():
        assert k in input_dict

    for k in input_dict.keys():
        X.append(input_dict[k])
        y.append(output_dict.get(k, 0))

    return np.array(X), np.array(y)
def test_classifier(clf, X, Y):
    folds = StratifiedKFold(Y, 20)
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

    print X
    print Y
    clf = linear_model.SGDClassifier(loss='log')
    test_classifier(clf, X, Y)

    clf = GaussianNB()
    test_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    test_classifier(clf, X, Y)

if __name__ == '__main__':
    main()
