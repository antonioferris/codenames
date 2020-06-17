'''
    This file defines the API of the GameState, which records the available information to
    Guessers and Masterminds.

    Masterminds know 25 words and their assignment as Red, Blue, Neutral, or Assassin

    Guessers simply know the remaining unguessed words.


    A public game state is simply a list of words
    e.g. pub_game_state = ['hairy', 'golf', 'China', 'Moscow', 'bottle']


    A private game state is a dictionary from words to their assignment
    e.g. priv_game_state = {'hairy' : 'red', 'golf' : 'neutral', 'China' : 'assassin', 'Moscow' : 'red', 'bottle' : 'blue'}
    The 4 keywords are:
    'red', 'blue, 'neutral', and 'assassin'
'''