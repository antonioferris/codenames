import numpy as np
import pickle
from scipy.spatial.distance import cosine, cdist
import random
import os, sys
from matplotlib import pyplot as plt
import itertools
sys.path.append('..')
import CreateEmbed

class AntMaster():

    # TODO KNOWN ERROR: New York not in corpus but is in the Codenames vocab

    '''
        color : team this agent tries to maake clues for
        corpus : file containing words that this corpus used for clues
        verbose : bool, prints more if true
        fast : speeds up computation at the expense of accuracy
    '''
    def __init__(self, color, corpus, verbose=False, fast=False):
        self.color = color
        self.verbose = verbose
        self.fast = fast

        embed_path = 'embeddings/' + corpus + '.embed'
        corpus_path = 'vocabs/' + corpus + '.txt'
        model_path = 'models/GoogleNews-vectors-negative300.bin'
        # create the word embeddings if not already existing
        if not os.path.exists(embed_path):
            CreateEmbed.save_embed(corpus_path, embed_path, model_path, verbose)

        # load the word embeddings
        with open(embed_path, 'rb') as f:
            self.word_embed = pickle.load(f)
        self.threshold = 0.5

        # load in all words from the corpus
        self.corpus = []
        with open(corpus_path, 'r') as f:
            for line in f:
                word = line[:-1]
                # remove words from corpus that aren't in our embeding
                if word not in self.word_embed:
                    continue
                self.corpus.append(word)
        

    '''
        Convert the game state into embeddings
        and lists of "good" and "bad" words to guess
    '''
    def convert_to_vectors(self, game_state):
        good_embed = []
        bad_embed = []
        good = []
        bad = []
        for word, val in game_state.items():
            if val == self.color:
                good_embed.append(self.word_embed[word])
                good.append(word)
            else:
                bad_embed.append(self.word_embed[word])
                bad.append(word)
        good_embed, bad_embed = np.array(good_embed), np.array(bad_embed)
        return good_embed, bad_embed, good, bad

    '''
        Make sure that the given word is not
        a copy of a word in the game
    '''
    def is_legal_word(self, word):
        return word not in self.restricted_words

    '''
        Defines the score of a clue by the threshold between the
        maximum word2vec cosine similiarity of the avoids and the
        minimum word2vec cosine similiarity of the picks
        (all parameters are word embeddings)
    '''
    def create_score_function(self, similiarity_measure):
        if similiarity_measure == 'cosine':
            sim_func = cosine
        elif similiarity_measure == 'l2':
            def sim_func(a, b):
                return np.linalg.norm(a - b)
        def score_func(clue, picks, avoids):
            max_dist = -10 # the maximum similiarity among our avoids
            min_dist = 10 #the minimum similiarity among our top picks
            for v in picks:
                if (d := sim_func(clue, v)) < min_dist:
                    min_dist = d
            for v in avoids:
                if (d := sim_func(clue, v)) > max_dist:
                    max_dist = d
            return min_dist - max_dist
        return score_func

    '''
        Given picks, avoids, and a score function
        attempt_clue will find the word that
        maximizes the score function
    '''
    def attempt_clue(self, picks, avoids, score_func):
        best_score = -np.Inf
        best_clue = None
        for word in self.corpus:
            if not self.is_legal_word(word):
                continue
            embed = self.word_embed[word]
            if (s := score_func(embed, picks, avoids)) > best_score:
                best_score = s
                best_clue = word
        return best_clue, best_score


    '''
        Given a private_game_state, a score function, 
        and a k, will attempt to find the best k words 
        to give a guess for
    '''
    def attempt_k_guess(self, k, private_game_state, score_func):
        good_embed, bad_embed, good, bad = self.convert_to_vectors(private_game_state)
        remaining = len(good)

        best_clue, best_score, best_words = None, -np.Inf, None
        # for each combination of k words chosen from out remaining words
        for idxs in itertools.combinations(range(remaining), k):
            # attempt a clue for the given word picks 
            clue, score = self.attempt_clue(good_embed[idxs, :], bad_embed, score_func)
            words = [good[idx] for idx in idxs]
            if self.verbose:
                print('For', *words, 'gave clue', clue, 'with score', score)

            if score > best_score:
                best_clue = clue
                best_score = score
                best_words = words

            # if we are in fast mode, only try 1 combination
            if self.fast:
                break
        return best_clue, best_score, best_words

    def give_clue(self, private_game_state):
        self.restricted_words = private_game_state.keys()
        clue, score, words = self.attempt_k_guess(2, private_game_state, self.create_score_function('cosine'))

        if self.verbose:
            print('Final Clue:', clue, 'for', *words)
            print('this clue had score', score)
            clue_embed = self.word_embed[clue]
            for word in private_game_state.keys():
                word_embed = self.word_embed[word]
                cos = cosine(word_embed, clue_embed)
                print(word, 'cosine', cos, 'l2', np.linalg.norm(clue_embed - word_embed))
        return clue, 2


def simple_test():
    game_state = {'president' : 'blue', 'queen' : 'blue', 'apple' : 'assassin', 'bottle' : 'red'}
    master = AntMaster('blue', '5k_common', verbose=False)
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
    simple_test()
    # embed_test()

if __name__ == '__main__':
    main()