# -*- coding: utf-8 -*-
from src import load_data, tokenizer
import math


def laplace_smooth(bigramCount, unigramCount, vocab):
    return math.log((bigramCount + 0.1) * 1.0 / (unigramCount + 0.1 * vocab))


class LHPSegmenter(object):
    def __init__(self, base_dir='./data'):
        self.vn_dict = set()
        self.unigram = {}
        self.bigram = {}
        self.load_dataset(base_dir)

    def load_dataset(self, base_dir):
        self.vn_dict = load_data.load_dictionary(base_dir)
        self.unigram = load_data.load_unigram(base_dir)
        self.bigram = load_data.load_bigram(base_dir)
        print(len(self.vn_dict))
        print(len(self.unigram))
        print(len(self.bigram))

    def compute_bigram(self, curWord, preWord):
        bi_count = 0
        if (preWord + curWord) in self.bigram:
            bi_count = self.bigram[preWord + curWord]
        uni_count = 0
        if preWord in self.unigram:
            uni_count = self.unigram[preWord]
        return laplace_smooth(bi_count, uni_count, len(self.unigram))