#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from q1 import build_lexicon
from q2 import count_ngrams
from q3 import calculate_perplexity_from_ngrams_model, predict_word_ngrams

def n1grams(old, n):
    new = {}
    for ngram in old:
        if len(ngram) != n:
            if ngram in new:
                new[ngram] += old[ngram]
            else:
                new[ngram] = old[ngram]
        else:
            ngram1 = ngram[1:]
            if ngram1 in new:
                new[ngram1] += old[ngram]
            else:
                new[ngram1] = old[ngram]

    return new


def predict_word(sequence_of_words, dict_ngrams, lexicon, n=3):
    """
    Provides a dictionary of the possible next words
    (list_considered_words) where the keys are the words from the
    lexicon and where the values are their estimated probability
    given n-1 words (sequence_of_words)

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
        integer that defines the order of the N-gram

    Returns
    -------
    dict_next_word: dict
        dictionary where keys are the possible next word and
        values are their estimated probability
    """
    if n == 0:
        index = -1
        for i in range(len(lexicon)):
            if lexicon[i] == '<s>':
                index = i
                break

        if index == -1:
            return {w: 1 / len(lexicon) for w in lexicon}
        else:
            ret = {w: 1 / (len(lexicon) - 1) for w in lexicon}
            ret['<s>'] = 0
            return ret


    dc = 0.422  # computed from n1, n2 in the original text

    ctr = 0

    Chw = {}
    l = len(lexicon)
    if '<s>' in lexicon:
        l -= 1
    for w in lexicon:
        tup = tuple(sequence_of_words + [w])
        if tup in dict_ngrams:
            ctr += 1
            Chw[w] = dict_ngrams[tup]
        else:
            Chw[w] = 0

    Ch = sum(Chw.values())

    newdict = n1grams(dict_ngrams, n)
    if Ch == 0:
        return predict_word(sequence_of_words[1:], newdict, lexicon, n-1)
    else:
        Phatwh = {w: 0 for w in lexicon}
        gamma = ctr * (dc / Ch)
        pbackoff = predict_word(sequence_of_words[1:], newdict, lexicon, n-1)
        for w in lexicon:
            if w != '<s>':
                Phatwh[w] = max(0, (Chw[w] - dc) / Ch) + gamma * pbackoff[w]

        return Phatwh


if __name__ == '__main__':
    lexicon = [i for i in build_lexicon(open('q4-data/train.txt', 'r'))]
    n = 3
    dict_ngrams = count_ngrams(open('q4-data/train.txt', 'r'), n)

    lopw = open('q4-data/correction.txt', 'r').readlines()[0].split()

    print(calculate_perplexity_from_ngrams_model(open('q4-data/testing.txt', 'r'),
                                                 dict_ngrams,
                                                 lexicon,
                                                 n,
                                                 lopw,
                                                 predict_word_ngrams))