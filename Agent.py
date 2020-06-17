'''
    This file defines the API of the 2 roles in Codenames:
        Masterminds and Guessers
'''


class Mastermind():

    '''
        Initializes a mastermind as a color
        'red', or 'blue'
    '''
    def __init__(self, color):
        pass

    '''
        Given a game state, a mastermind returns a single english
        word as a clue, and a number of words the clue pertains to.
    
        returns a tuple (clue_word, num_words)
    '''
    def give_clue(self, private_game_state):
        pass


class Guesser():

    '''
        Given a clue and a public game state, a guesser
        will return a list of guesses given the clue
        (and potentially past clues as well)

        returns a list of english words
    '''
    def guess(self, clue, public_game_state):
        pass
