import numpy as np
import pickle
from scipy.spatial.distance import cosine
import random
import os
from matplotlib import pyplot as plt
from .. import create_embed

class AntMaster():

    def __init__(self, color, corpus):
        self.color = color

        embed_path = '../embeddings/' + corpus + '.embed'
        corpus_path = '../vocabs/' + corpus
        # load in the word embeddings
        if not os.path.exists(embed_path):

        with open(, 'rb') as f:
            self.word_embed = pickle.load(f)
        self.threshold = 0.5

        # load in all words from the corpus
        self.corpus = []
        with open(corpus_path, 'r') as f:
            for line in f:
                self.corpus.append(line[:-1])
        

    def convert_to_vectors(self, game_state):
        good = []
        bad = []
        for word, val in game_state:
            if val == self.color:
                good.append(self.word_embed[word])
            else:
                bad.append(self.word_embed[word])
        good, bad = np.array(good), np.array(bad)
        return good, bad


    def give_clue(self, private_game_state):
        good, bad = self.convert_to_vectors(private_game_state)


        return 'eggs'




def simple_test():
    game_state = {'president' : 'blue', 'queen' : 'blue', 'ditch' : 'assassin', 'bottle' : 'red'}
    master = AntMaster('blue')
    print('Game State', game_state)
    print('Clue', master.give_clue(game_state))

def embed_test():
    with open('../models/word_embeddings.pickle', 'rb') as f:
        word_embed = pickle.load(f)
    words = []
    with open('../clean_words.txt') as f:
        for line in f:
            words.append(line[:-1])
    word_test = ['egg', 'China', 'knight']
    for word in word_test:
        max_sim = -1
        max_word = None
        for word2 in words:
            sim = cosine(word_embed[word], word_embed[word2])
            if sim > max_sim:
                max_sim = sim
                max_word = word2
        print(word, max_word, max_sim)



def main():
    # simple_test()
    embed_test()

if __name__ == '__main__':
    main()