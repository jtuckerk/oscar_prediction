# conda install scikit-learn
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold
from sklearn import metrics 

# omdb_responses: ['id','title','year','crit_score','cons_score',...]
def load_rotten():
    f = open('data/omdb_data.txt', 'r') #omdb_responses/omdb_responses_full', 'r')
    lines = f.readlines()
    f.close()

    rotten = []
    for line in lines: 
        line = eval(line)
        rotten.append(line)
    
    return rotten


# oscar_y: (('title',year), num_wins_noms)
def load_oscars(): 
    f = open('data/oscar_y_full.txt', 'r')
    lines = f.readlines()
    f.close()

    oscars = {}
    for line in lines:
        line = eval(line)
        movie, year = line[0]
        num = line[1]
        if num >= 1: 
            oscars[(movie, str(year))] = 1
    
    return oscars


def load():
    return load_rotten(), load_oscars()


def create_input(rotten):
    # id, title, year, critscore, conscore, media type, runtime, metascore, released, imdb rating, imdb votes, box office, country 
    # only include year, critscore, conscore (metascore, imdb rating) 
    SKIP = 3 
    WIDTH = 4 #2 # len(rotten[0]) - SKIP  
    X = scipy.zeros((len(rotten), WIDTH))
    for i in range(0, len(rotten)): 
        for j in range(3, 5): #(SKIP, WIDTH): 3,5 for just rotten
            X[i, j-SKIP] = rotten[i][j] if rotten[i][j] != 'N/A' else 0
    print "total movies", len(rotten)
    return X 
    
def create_output(rotten, oscars):
    Y = scipy.zeros(len(rotten)) 
    for i in range(0, len(rotten)): 
        movie = rotten[i][1]
        year = rotten[i][2]
        if (movie, year) in oscars: 
            Y[i] = 1 
    print 'num of oscar noms', sum(Y)
    return Y 


def test_classifier(clf, X, Y):
    folds = StratifiedKFold(Y, 5)
    aucs = []
    for train, test in folds:
        # Sizes
        # print X[train].shape, Y[train].shape
        # print X[test].shape, len(prediction)

        clf.fit(X[train], Y[train])
        prediction = clf.predict_proba(X[test])
        aucs.append(roc_auc_score(Y[test], prediction[:, 1]))
    print clf.__class__.__name__, aucs, numpy.mean(aucs)


def baseline(rotten, oscars): 
    # certified fresh - crit score 75% or higher --> nomination 
    Z = scipy.zeros(len(rotten))
    W = scipy.zeros(len(rotten))
    V = scipy.zeros(len(rotten))
    U = scipy.zeros(len(rotten))
    for i in range(0, len(rotten)):
        movie = rotten[i][1]
        year = rotten[i][2]
        critscore = rotten[i][3]
        
        if (int(critscore) >= 75) and ((movie, year) in oscars): 
            Z[i] = 1
        if (int(critscore) >= 75) and not ((movie, year) in oscars):
            W[i] = 1
        if (int(critscore) < 75) and ((movie, year) in oscars): 
            V[i] = 1
        if (int(critscore) < 75) and not ((movie, year) in oscars): 
            U[i] = 1
    
    #print 'num of true positives', 
    tp = sum(Z)
    #print 'num of false positives', 
    fp = sum(W)
    #print 'num of false negatives', 
    fn = sum(V)
    #print 'num of true negatives', 
    tn = sum(U)
    #true pos rate 
    tpr = tp / (tp + fn) 
    #false pos rate
    fpr = fp / (fp + tn) 
    
    #area of trapezoid
    auc = tpr * ((1-fpr) + 1) / 2
    print "baseline AUC:", auc, tp, fp, fn, tn
            

def main():
    
    rotten, oscars = load()
    X = create_input(rotten)
    Y = create_output(rotten, oscars)
    
    clf = linear_model.SGDClassifier(loss='log')
    test_classifier(clf, X, Y)

    clf = GaussianNB()
    test_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    test_classifier(clf, X, Y)

    baseline(rotten, oscars)


if __name__ == '__main__':
    main()
