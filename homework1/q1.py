#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def build_lexicon(corpus_object):
    lexicon = {} # create an empty lexicon
    for line in corpus_object.readlines() :   # scan each line
        for word in line.split():    # split line into words
            if word not in lexicon :
                lexicon[word] = 1    # add word to lexicon if needed
            else :
                lexicon[word] += 1    # or increment the counter for the word

    return lexicon


def get_ordered_list_frequent_words(lexicon_dict, k):
    """
    Provides a list of the k most frequent words ordered by
    decreasing frequency and where ties are broken thanks to
    alphabetical ordering

    Parameters
    -----------
    lexicon_dict: dict
        Dictionary where the keys are strings and the values are integers

    Returns
    -------
    ordered_words: list of strings
        List of the ordered words
    """

    return sorted(sorted(lexicon_dict), key=lexicon_dict.get, reverse=True)[:k]


def build_TRAIN(top_freq):
    fo = open('train.txt', 'r')
    fo2 = open('train_processed.txt', 'w+')

    s = ''
    for line in fo.readlines() :   # scan each line
        s += '<s> '
        for word in line.split():    # split line into words
            if word in top_freq:
                s += word + ' '
            else :
                s += '<UNK> '
        s += '</s>\n'

    fo2.write(s)

    return fo2.close()


def OOV_rate(lexicon_dict):
    """
    Compute the OOV rate, which is the relative frequency of
    occurrence of the <UNK> token in the training corpus

    Parameters
    -----------
    lexicon_dict: dict
        Dictionary where the keys are strings and the values are integers

    Returns
    -------
    OOV_rate: float
    """

    return lexicon_dict['<UNK>'] / sum(lexicon_dict.values())


if __name__ == '__main__':
    file_object = open('train.txt', 'r')
    lexicon = build_lexicon(file_object)
    file_object.close()

    print('number of distinct tokens:', len(lexicon))


    ctr1 = 0
    ctr2 = 0
    for w in lexicon:
        if lexicon[w] == 1:
            ctr1 += 1
        if lexicon[w] == 2:
            ctr2 += 2


    top10k = get_ordered_list_frequent_words(lexicon, 10_000)

    build_TRAIN(set(top10k))

    fo2 = open('train_processed.txt', 'r')
    lexicon2 = build_lexicon(fo2)

    print('OOV rate:', 100*OOV_rate(lexicon2))

