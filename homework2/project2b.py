#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import nltk

def get_homographs_one_word(corpus, the_word):
    """
    Provides the different PoS tags for a given word

    Parameters
    -----------
    corpus: a `TaggedCorpusReader` object created from some
        text representation of the corpus (i.e. BAWE_train)
    the_word: string
        word for which we want to retrieve the PoS tags

    Returns
    -------
    pos_tags: set of PoS tags for the_word
    """

    pos_tags = set()

    tagged_words_corpus = corpus.tagged_words()
    for word, tag in tagged_words_corpus:
        if word == the_word:
            pos_tags.add(tag)

    return pos_tags