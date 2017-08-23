import math

def laplace_smooth(bigramCount, unigramCount, vocab):
    return math.log((bigramCount + 0.1) * 1.0 / (unigramCount + 0.1 * vocab))

class WSGraph(object):
    def __init__(self, processed_sentence, vn_dict, unigram, bigram):
        self.sentence = '<s> ' + processed_sentence + ' <e>'
        self.unigram = unigram
        self.bigram = bigram
        self.tokens = self.sentence.split(' ')
        self.n = len(self.tokens)

        self.vertexes = []
        self.edges = {}
        self.vn_dict = vn_dict
        self.maxAt = []
        self.maxEdgeAt = []
        self.maxPreEdgeAt = {}

    def compute_bigram(self, curWord, preWord):
        bi_count = 0
        if (preWord + curWord) in self.bigram:
            bi_count = self.bigram[preWord + curWord]
        uni_count = 0
        if preWord in self.unigram:
            uni_count = self.unigram[preWord]
        return laplace_smooth(bi_count, uni_count, len(self.unigram))

    def compute_bigram_edge(self, curEdge, preEdge):
        if curEdge == preEdge:
            return 0
        return self.compute_bigram(self.edge_to_word(curEdge), self.edge_to_word(preEdge))

    def sub_to_word(self, i, j):
        return '_'.join(self.tokens[i: j + 1])

    def edge_to_word(self, edge):
        if edge[0] == 0 and edge[1] == 0:
            return '<s>'
        if edge[1] == self.n - 1 and edge[0] == self.n - 1:
            return '<e>'
        return '_'.join(self.tokens[edge[0] + 1: edge[1] + 1])

    def construct_graph(self):
        for i in range(0, self.n - 1):
            self.vertexes.append(i)
            self.maxAt.append(0)
            if i > 0:
                self.maxEdgeAt.append((i, i + 1))
            else:
                self.maxEdgeAt.append((0, 0))
            self.edges[i] = []
        for i in range(0, self.n):
            for j in range(i + 1, min(i + 4, self.n)):
                if self.edge_to_word((i, j)) in self.vn_dict:
                    self.edges[j].append((i, j))
        for i in range(1, self.n - 1):
            if len(self.edges[i]) == 0:
                self.edges[i].append((i - 1, i))
        self.edges[0] = [(0, 0)]
        # self.edges[self.n - 1] = [(self.n - 1, self.n - 1)]

    def compute_shortest_path(self):
        self.maxPreEdgeAt[(0, 0)] = (0, 0)
        for i in range(1, self.n - 1):
            v_edges = self.edges[i]
            cur_max = float('-inf')

            for edge in v_edges:
                cur_pre_max = float('-inf')
                for pre_edge in self.edges[edge[0]]:
                    # bigram_prob = self.compute_bigram(
                    #     self.edge_to_word(edge),
                    #     self.edge_to_word(self.maxEdgeAt[edge[0]]))
                    # prob = self.maxAt[edge[0]] + bigram_prob
                    # if prob > cur_max:
                    #     cur_max = prob
                    #     self.maxAt[i] = cur_max
                    #     self.maxEdgeAt[i] = edge
                    bigram_prob = self.compute_bigram_edge(edge, pre_edge)
                    pre_bigram_prob = self.compute_bigram_edge(pre_edge, self.maxPreEdgeAt[pre_edge])
                    prob = self.maxAt[self.maxPreEdgeAt[pre_edge][1]] + bigram_prob + pre_bigram_prob
                    if prob > cur_max:
                        cur_max = prob
                        self.maxAt[i] = cur_max
                        self.maxEdgeAt[i] = edge
                    if prob > cur_pre_max:
                        self.maxPreEdgeAt[edge] = pre_edge
                        cur_pre_max = prob

    def to_output(self):
        i = self.n - 2
        print(self.maxAt[self.n - 2])
        maxEdge = self.maxEdgeAt[i]
        result = self.edge_to_word(maxEdge) + ' '
        while i > 0:
            maxEdge = self.maxPreEdgeAt[maxEdge]
            result = self.edge_to_word(maxEdge) + ' ' + result
            i = maxEdge[0]
        return result.strip()
