import numpy as np
import gensim

from gensim.models import Word2Vec


class AntMaster():

    def __init__(self, color):
        self.color = color

    def give_clue(self, private_game_state):
        return 'eggs'




def simple_test():
    game_state = {'president' : 'blue', 'queen' : 'blue', 'ditch' : 'assassin', 'bottle' : 'red'}
    master = AntMaster('blue')
    print('Game State', game_state)
    print('Clue', master.give_clue(game_state))

def main():
    simple_test()

if __name__ == '__main__':
    main()