# -*- coding: utf-8 -*-
from src import load_data, tokenizer, ws_graph
import math


def laplace_smooth(bigramCount, unigramCount, vocab):
    return math.log((bigramCount + 0.1) * 1.0 / (unigramCount + 0.1 * vocab))


class Segmenter(object):
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

    def compute_prob_sent(self, sentence):
        sentence = "<s> " + sentence
        tokens = sentence.split(" ")
        prob = 0.0
        for index in range(0, len(tokens) - 1):
            prob += self.compute_bigram(tokens[index + 1], tokens[index])
        return prob

    def match_left_to_right(self, sentence):
        tokens = sentence.split(" ")
        result = []
        i = 0
        while i < len(tokens):
            if '_' in tokens[i]:
                result.append(tokens[i])
                i = i + 1
            else:
                word = tokens[i]
                max_word = word
                index = i
                count = 0
                for j in range(i + 1, len(tokens)):
                    word += "_" + tokens[j]
                    count = count + 1
                    if count == 5:
                        break
                    if word.lower() in self.vn_dict:
                        max_word = word
                        index = j
                result.append(max_word)
                i = index + 1

        sentence = ""
        for j in range(0, len(result)):
            sentence += result[j] + " "
        return sentence.strip()

    def match_right_to_left(self, sentence):
        tokens = sentence.split(" ")
        result = []
        i = len(tokens) - 1
        while i >= 0:
            if '_' in tokens[i]:
                result.append(tokens[i])
                i = i - 1
            else:
                word = tokens[i]
                max_word = word
                index = i
                count = 0
                i = i - 1
                while i >= 0:
                    word = tokens[i] + "_" + word
                    count = count + 1
                    if count == 5:
                        break
                    if word.lower() in self.vn_dict:
                        max_word = word
                        index = i
                    i = i - 1
                result.append(max_word)
                i = index - 1
        j = len(result) - 1
        sentence = ""
        while j >= 0:
            sentence += result[j] + " "
            j = j - 1
        return sentence.strip()

    def generate_overlap_cases(self, sentence):
        cases = []
        left = self.match_left_to_right(sentence)
        right = self.match_right_to_left(sentence)
        if left == right:
            cases.append(left)
        else:
            cases.append(left)
            cases.append(right)
        return cases

    def generate_conjuntion_cases(self, sentence):
        overlapCases = self.generate_overlap_cases(sentence)
        conjunctionCases = []
        for i in range(0, len(overlapCases)):
            tokens = overlapCases[i].split(" ")
            for j in range(0, len(tokens)):
                syls = tokens[j].split("_")
                if len(syls) == 2:
                    tokens[j] = syls[0]+" "+syls[1]
                    conjunctionCases.append(' '.join(tokens).strip())
                if len(syls) == 3:
                    if (syls[0]+"_"+syls[1]) in self.vn_dict and syls[2] in self.vn_dict:
                        s = overlapCases[i].replace(tokens[j], syls[0]+"_"+syls[1]+" "+syls[2])
                        conjunctionCases.append(s)
                    if (syls[1]+"_"+syls[2]) in self.vn_dict and syls[0] in self.vn_dict:
                        s = overlapCases[i].replace(tokens[j], syls[0]+" "+syls[1]+"_"+syls[2])
                        conjunctionCases.append(s)
        return conjunctionCases

    def generateAllAmbiguities(self, sentence):
        ambiCases = []
        overlapCases = self.generate_overlap_cases(sentence)
        conjunctionCases = self.generate_conjuntion_cases(sentence)
        ambiCases = ambiCases + overlapCases + conjunctionCases
        print(overlapCases)
        print(conjunctionCases)
        return ambiCases

    def chooseBestCase(self, sentence):
        ambiCases = self.generateAllAmbiguities(sentence)
        maxProb = -999999.0
        bestCase = ""
        for i in range(0, len(ambiCases)):
            prob = self.compute_prob_sent(ambiCases[i])
            print(ambiCases[i], prob)
            if prob > maxProb:
                maxProb = prob
                bestCase = ambiCases[i]
        return bestCase

    def graph_dynamic_programing(self, sentence):
        graph = ws_graph.WSGraph(sentence, self.vn_dict, self.unigram, self.bigram)
        graph.construct_graph()
        graph.compute_shortest_path()
        return graph.to_output()

    def segmentSentence(self, sentence):
        sentence = tokenizer.tokenizer_sentence(sentence)
        return self.chooseBestCase(sentence)
    

if __name__ == '__main__':
    seg = Segmenter('../data')
    # print(seg.graph_dynamic_programing('học sinh học sinh học'))
    print(seg.graph_dynamic_programing('tốc độ truyền thông tin ngày càng cao'))
    # print(seg.graph_dynamic_programing('con ngựa đá con ngựa đá'))
    # print(seg.graph_dynamic_programing('con ruồi đậu mâm'))
    print(seg.compute_prob_sent('tốc_độ truyền_thông tin ngày_càng cao'))
    print(seg.compute_prob_sent('tốc_độ truyền thông_tin ngày_càng cao'))
