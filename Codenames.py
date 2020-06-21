'''
    This file defines functions capable of running a full
    codenames game between various Agents defined in the
    agents folder.
'''
import csv
import random
from agents.AntAgents import AntMaster
# load the codenames vocabulary
def get_words():
    words = []
    with open('vocabs/codenames_vocab.txt', 'r') as f:
        for line in csv.reader(f):
            words.append(line[0])
    return words


def show_game_state(game_state):
    # check if we are a private or public game state
    if isinstance(game_state, list):
        private = False
    else:
        private = True

    if private:
        strings = [key + ':' + val for key, val in game_state]
    else:
        strings = game_state

    # if the game state is short, just print it on one line
    if len(strings) <= 5:
        print(' '.join(strings))
        return

    row_size = 5
    rows = []
    i = 0
    for s in strings:
        if i % row_size == 0:
            rows.append([])
        rows[-1].append(s)
        i += 1


    maxes = [0] * 5
    for col in range(row_size):
        for row in rows:
            if len(row) > col:
                maxes[col] = max(maxes[col], len(row[col]))
    for row in rows:
        s = ''
        for col in range(len(row)):
            to_add = row[col]
            if len(to_add) < maxes[col]:
                to_add += ' ' * (maxes[col] - len(to_add))
            s += to_add
            if col != 4:
                s += '  '
        print(s)
    print()

# returns a tuple of (first, public_game_state, private_game_state)
# where first is the color of the first player
def init_game():
    words = get_words()

    # get 25 random words
    public_game_state = random.sample(words, 25)
    assignments = list(range(25))
    random.shuffle(assignments)

    # randomly assign these 25 words
    private_game_state = dict(zip(public_game_state, assignments))

    if random.random() > 0.5:
        first = 'blue'
    else:
        first = 'red'
    
    # conver thet int assignments to their english counterparts
    for word, idx in private_game_state.items():
        if idx < 6:
            roll = 'red'
        elif idx == 6:
            roll = first
        elif idx < 13:
            roll = 'blue'
        elif idx < 24:
            roll = 'neutral'
        else:
            roll = 'assassin'
        private_game_state[word] = roll
    return first, public_game_state, private_game_state

# Iteratively collect the player's guesses from the previous clue
def get_input_words(full_game_state, color, k):
    public_game_state, private_game_state = full_game_state
    for i in range(k+1):
        guess = input('Please guess a word, or press enter to pass the turn\n$ ')
        while guess not in public_game_state and guess != '':
            guess = input('Guess not one of the words remaining.  Please re-enter your guess or enter an empty guess to pass the turn\n$ ')
        if guess == '':
            break
        roll = private_game_state[guess]
        print(guess, 'was', roll)
        # if roll is assassin, the other team wins
        if roll == 'assassin':
            return opp(color)
        public_game_state.remove(guess)
        private_game_state.pop(guess)
        if roll != color:
            break
        

        # if we have no agents left, we win!
        if color not in private_game_state.values():
            return color
    
    # if no one won, return the next game state
    return public_game_state, private_game_state
        

def run_turn(color, mastermind, full_game_state):
    public_game_state, private_game_state = full_game_state
    print(color + "'s turn")
    clue, k = mastermind.give_clue(private_game_state)
    print('Current Available words: ')
    show_game_state(public_game_state)
    print('Clue:', clue, 'for', k)
    print('Guessing for', color, 'team')
    full_game_state = get_input_words(full_game_state, color, k)
    return full_game_state

def opp(color):
    if color == 'red':
        return 'blue'
    return 'red'

def win(color):
    print('Congratulations', color, 'You have won the game!')
            
def run_game():
    player, public_game_state, private_game_state = init_game()
    full_game_state = (public_game_state, private_game_state)
    agents = {
        'red' : AntMaster('red', '5k_common', verbose=True, fast=True),
        'blue' : AntMaster('blue', '5k_common', verbose=True, fast=True)
    }
    while True:
        full_game_state = run_turn(player, agents[player], full_game_state)
        if isinstance(full_game_state, str): # if the game state is a string, then someone won the game
            winner = full_game_state
            win(winner)
            break
        player = opp(player)
        print()





def main():
    run_game()


if __name__ == '__main__':
    main()