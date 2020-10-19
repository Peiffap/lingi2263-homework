#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from q2 import count_ngrams
import math


def predict_word_ngrams(sequence_of_words, dict_ngrams, lexicon, n):
    """
    Provides a dictionary of the possible next words where the keys
    are the words from the lexicon and where the values are their
    estimated probability given n-1 words (sequence_of_words)

    Parameters
    -----------
    sequence_of_words: list
        List of (up to) n-1 words
    dict_n-grams: dict
        Dictionary that contains all the n-grams from the corpus
        along with their frequency counts.
    lexicon: list
        List of word types
    n: int
        integer that defines the order of the N-gram model

    Returns
    -------
    dict_next_word: dict
        dictionary where keys are the possible next word and values
        are their estimated probability
    """
    dict_next_word = {} # TODO: Compute the appropriate value
    Ch = 0
    Chw = {}
    l = len(lexicon)
    if '<s>' in lexicon:
        l -= 1
    for w in lexicon:
        tup = tuple(sequence_of_words + [w])
        if tup in dict_ngrams:
            Chw[w] = dict_ngrams[tup]
            Ch += dict_ngrams[tup]
        else:
            Chw[w] = 0

    for w in lexicon:
        if w == '<s>':
            dict_next_word['<s>'] = 0
        else:
            dict_next_word[w] = (Chw[w] + 1) / (Ch + l)

    return dict_next_word


def calculate_perplexity_from_ngrams_model(corpus_object_missing, dict_ngrams, lexicon, n, list_of_predicted_words, model=predict_word_ngrams):
    """
    Provides the (average) perplexity of a probability distribution
    model of missing words

    Parameters
    -----------
    corpus_object_missing: object
        file object returned by open('filename') where some words
        have been replaced by the string <MIS>
    dict_n-grams: dict
        Dictionary that contains all the n-grams from the corpus
        along with their frequency counts.
    lexicon: list
        List of word types
    n: int
        Integer that defines the order of the N-gram model
    list_of_predicted_words: list of strings
        List of the correct missing tokens in the corpus. In other
        words, `list_of_predicted_words[i]` is the value of the
        words from the original corpus that has been replaced by
        the i-th occurrence of '<MIS>' in the modified corpus.

    Returns
    -------
    perplexity: float
        Float that provides the perplexity of the model
    """
    histories = []

    for i in range(len(list_of_predicted_words)):
        if list_of_predicted_words[i] not in lexicon:
            list_of_predicted_words[i] = '<UNK>'


    def replace_MIS(arr, ind):
        new_ind = ind
        new_arr = arr[:]
        for i in range(len(arr)):
            if arr[i] == '<MIS>':
                new_arr[i] = list_of_predicted_words[new_ind]
                new_ind += 1

        return new_ind, new_arr

    index = 0
    for line in corpus_object_missing.readlines() :   # scan each line
        l = line.split()
        for j in range(min(len(l), n)):
            if l[j] == '<MIS>':
                index, l[:j] = replace_MIS(l[:j], index)
                histories += [l[:j]]

        i = 1
        while i+n <= len(l):
            if l[i+n-1] == '<MIS>':
                index, l[i:i+n] = replace_MIS(l[i:i+n], index)
                histories += [l[i:i+n-1]]
            i += 1


    LL = 0
    for i in range(len(histories)):
        h = histories[i]
        preds = model(h, dict_ngrams, lexicon, n)
        LL += math.log2(preds[list_of_predicted_words[i]])

    PP = math.pow(2, -LL / len(histories))

    return PP

if __name__ == '__main__':
    dict_ngrams = {('hi', 'buddy'): 2,
           ('hi', 'fella'): 1}
    sow = ['hi']
    lexicon = ['buddy', 'fella', 'gamer', '<s>']
    print(predict_word_ngrams(sow, dict_ngrams, lexicon, 2))

    com = open('train_processed_missing.txt', 'r')
    n = 3
    dict_ngrams = count_ngrams(com, n)
    com = open('train_processed_missing.txt', 'r')
    lexicon = ['<s>', '</s>', '<UNK>', 'pal', 'man', 'dude']
    lopw = ['pal', 'dude', '<UNK>']
    print(calculate_perplexity_from_ngrams_model(com, dict_ngrams, lexicon, n, lopw))