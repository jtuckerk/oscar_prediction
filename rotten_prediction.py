# conda install scikit-learn
import scipy
import numpy
from sklearn import linear_model
from sklearn.metrics import roc_auc_score
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import StratifiedKFold


# player,year,stint,teamId,lgID,G,AB,R,H,2B,3B,HR,RBI,SB,CS,BB,SO,IBB,HBP,SH,SF,GIDP
# omdb_responses: ['id','title','year','crit_score','cons_score',...]
def load_rotten():
    f = open('omdb_responses/omdb_responses_full', 'r')
    lines = f.readlines()
    f.close()

    rotten = []
    for line in lines: 
        line = eval(line)
        rotten.append(line)
    
    #print rotten
    return rotten

# playerID,yearID,gameNum,gameID,teamID,lgID,GP,startingPos
# oscar_y: (('title',year), num_wins_noms)
def load_oscars(): 
    f = open('oscar_y/oscar_y_full', 'r')
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


def create_input(rotten): #def create_input(batting):
    # don't want to cinlude playerID, sting, team, league year in predicition
    '''SKIP = 5
    WIDTH = len(batting[0]) - SKIP
    X = scipy.zeros((len(batting), WIDTH))
    for i in range(0, len(batting)):
        for j in range(SKIP, WIDTH):
                X[i, j-SKIP] = batting[i][j] if batting[i][j] != '' else 0
    return X
    '''
    # id, title, year, critscore, conscore, media type, runtime, metascore, released, imdb rating, imdb votes, box office, country 
    # only include year, critscore, conscore
    SKIP = 3 
    WIDTH = 2 # len(rotten[0]) - SKIP  
    X = scipy.zeros((len(rotten), WIDTH))
    for i in range(0, len(rotten)): 
        for j in range(3,5): #(SKIP, WIDTH):
            X[i, j-SKIP] = rotten[i][j] if rotten[i][j] != 'N/A' else 0
    print X
    return X 
    
def create_output(batting, all_stars):
    Y = scipy.zeros(len(batting))
    for i in range(0, len(batting)):
        player = batting[i][0]
        year = batting[i][1]
        if (player, year) in all_stars:
            Y[i] = 1
    
    print 'Number of all stars', sum(Y)
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


def main():
    '''batting, all_stars = load()
    X = create_input(batting)
    Y = create_output(batting, all_stars)
    
    clf = linear_model.SGDClassifier(loss='log')
    test_classifier(clf, X, Y)

    clf = GaussianNB()
    test_classifier(clf, X, Y)

    clf = RandomForestClassifier(n_estimators=10, max_depth=10)
    test_classifier(clf, X, Y)
    '''
    rotten, oscars = load()
    X = create_input(rotten)

if __name__ == '__main__':
    main()
