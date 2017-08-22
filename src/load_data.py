# -*- coding: utf-8 -*-
import io

def load_dictionary(base_dir):
    vn_dict = set()
    with io.open(base_dir + '/dict.txt', mode='r', encoding='utf-8') as dict_file:
        lines = dict_file.readlines()
        for line in lines:
            line = line.strip()
            vn_dict.add(line)
    return vn_dict

def load_unigram(base_dir):
    unigram = {}
    with io.open(base_dir + '/ws_unigram.txt', mode='r', encoding='utf-8') as unifile:
        lines = unifile.readlines()
        for line in lines:
            line = line.strip()
            tokens = line.split(' ')
            if len(tokens) == 2:
                # unigram.put(tokens[0], Integer.parseInt(tokens[1]))
                unigram[tokens[0]] = int(tokens[1])
    return unigram

def load_bigram(base_dir):
    bigram = {}
    with io.open(base_dir + '/ws_bigram.txt', mode='r', encoding='utf-8') as bigramfile:
        lines = bigramfile.readlines()
        for line in lines:
            line = line.strip()
            tokens = line.split(' ')
            if len(tokens) == 3:
                bigram[tokens[0] + tokens[1]] = int(tokens[2])
    return bigram

# if __name__ == '__main__':
#     # dictionary = load_dictionary()
#     # print(len(dictionary))
#     unigram = load_unigram()
#     print(unigram[u'lượn'])