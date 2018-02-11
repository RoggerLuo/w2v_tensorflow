from sentence import Sentence
from wv import Wv
from config import Config
from dataset import Dataset
from db import Db
from nn.model import Nn
from negSampling import NegSampling
import numpy as np

import time
timeRecorder = 0


class Main(object):

    def __init__(self, config):
        self.sentence = Sentence(config)
        wv = Wv(config)
        self.db = Db(config, wv)
        self.dataset = Dataset(config, self.db)
        self.nn = Nn(config)
        self.negSampling = NegSampling(config)

        self.config = config

    def train_sentence(self, sentence):
        word_n_context_pairs = self.sentence.getWordAndContext(sentence)
        cost = 0
        for pair in word_n_context_pairs:
            cost += self.train_centerword_n_context_pair(pair)
        return cost

    def train_centerword_n_context_pair(self, pair):
        center = pair['word']
        contexts = pair['context']
        # print('training word:', center)
        cost = 0
        for target in contexts:
            cost_list = self.train_center_n_target(center, target)
            cost += np.sum(cost_list)
        return cost

    def train_center_n_target(self, center, target):
        c, t, n = self.dataset.get(center, target)  # 换取得到word vector的值

        # c, t, n = self.tensorflow_nn(c, t, n)
        c, t, n, cost_list = self.native_nn(c, t, n)

        self.dataset.set(c, t, n)  # 保存回去
        return cost_list

    def native_nn(self, c, t, n):
        # timeRecorder = time.time()
        c, t, n, cost_list = self.negSampling.train(c, t, n)
        # print(cost_list)
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
        self.db.save()


def test():
    string = "我爱北京天安门测试一下是不是正确，天安门上太阳升，父流程表单匹配字段中，说明文字控件不应该出现，上传文字和上传图片、日期区间控件父表单未筛选出来"
    main = Main(Config)
    for i in range(Config.repeate_times):
        cost = main.train_sentence(string)
        print(cost)
    main.save()
    # print(main.db.data)
test()
