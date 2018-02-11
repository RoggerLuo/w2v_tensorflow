from .sentence import Sentence
from .config import Config
from .dataset.dataset import Dataset
from .core.nn.model import Nn
from .core.negSampling import NegSampling
import numpy as np
import time
timeRecorder = 0


class Train(object):

    def __init__(self):

        self.sentence = Sentence(Config)
        self.dataset = Dataset(Config) 
        self.nn = Nn(Config)
        self.negSampling = NegSampling(Config)
        self.config = Config


    def sentence_str(self, string):
        word_n_context_pairs = self.sentence.getWordAndContext(string)
        cost = 0
        for pair in word_n_context_pairs:
            cost += self.centerword_n_context_pair(pair)
        return cost

    def centerword_n_context_pair(self, pair):
        center = pair['word']
        contexts = pair['context']
        # print('training word:', center)
        cost = 0
        for target in contexts:
            cost += self.center_n_target(center, target)
        return cost

    def center_n_target(self, center, target):
        c, t, n = self.dataset.get(center, target)  # 换取得到word vector的值

        # c, t, n = self.tensorflow_nn(c, t, n)
        c, t, n, cost = self.native_nn(c, t, n)

        self.dataset.set(c, t, n)  # 保存回去
        return cost

    def native_nn(self, c, t, n):
        # timeRecorder = time.time()
        c, t, n, cost_list = self.negSampling.train(c, t, n)
        # print('train 耗时：', time.time() - timeRecorder)
        return c, t, n, cost_list

    def tensorflow_nn(self, c, t, n):
        timeRecorder = time.time()
        self.nn.build(c, t, n)  # 一组center target negs
        print('build 耗时：', time.time() - timeRecorder)

        timeRecorder = time.time()
        c, t, n, cost_list = self.nn.train().export()
        print('train 耗时：', time.time() - timeRecorder)
        return c, t, n

    def save(self):
        self.dataset.save()

