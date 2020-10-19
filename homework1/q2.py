#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def count_ngrams(corpus_object, n):
    """ Provides a lexicon of the n-grams along with their count
    Parameters
    -----------
    corpus_object: file object returned by open('filename')
        file object that contains a text corpus
    n: int
        integer that define the length taken into account in the n-grams

    Returns
    -------
    dict_ngrams: dict
        Dictionary that contains all the n-grams from the corpus
        along with their count. The keys are tuples of strings
        and the values are integers.
    """

    dict_ngrams = {} # create an empty lexicon
    for line in corpus_object.readlines() :   # scan each line
        l = line.split()
        for j in range(1, min(len(l), n)):
            if tuple(l[:j]) in dict_ngrams:
                dict_ngrams[tuple(l[:j])] += 1
            else:
                dict_ngrams[tuple(l[:j])] = 1

        i = 0
        while i+n <= len(l):
            if tuple(l[i:i+n]) in dict_ngrams:
                dict_ngrams[tuple(l[i:i+n])] += 1
            else:
                dict_ngrams[tuple(l[i:i+n])] = 1

            i += 1

    return dict_ngrams


if __name__ == '__main__':
    fo = open('train_processed.txt', 'r')
    lex = count_ngrams(fo, 1)
    print(len(lex))
