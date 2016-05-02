from gensim import models
m = models.Word2Vec.load_word2vec_format('~/Desktop/w2v_model.w7s128.bin', binary=True)
