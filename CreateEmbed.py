'''
    This file will load in a specific subset of the words
    in the Google News Word2Vec dataset and pickle them
    to allow agents to more quickly load in word2vec models.
'''
import csv
import pickle
import gensim

'''
    Use the give Word2Vec model to save only the word
    embeddings of words in the file dictionary to output
    path
'''
def save_embed(dictionary, output_path, model_path, verbose=False):
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    words = set()
    with open(dictionary, 'r') as f:
        for line in csv.reader(f):
            words.add(line[0])

    # also add the codenames dictionary to every embedding
    with open('../vocabs/codenames_vocab.txt', 'r') as f:
        for line in csv.reader(f):
            words.add(line[0])

    embeds = {}
    for word in words:
        try:
            embeds[word] = model[word]
        except:
            if verbose:
                print(word, 'not in Word2Vec model')
    with open(output_path, 'wb') as f:
        pickle.dump(embeds, f)

def main():
    model = gensim.models.KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

    # save only the embeddings of the words in our Codenames dictionary
    save_embed(model, '../words.txt', 'word_embeddings.pickle')


if __name__ == '__main__':
    main()