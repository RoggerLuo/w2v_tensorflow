from sentence import Sentence
from wv import Wv
from config import Config
from dataset import Dataset
from db import Db
from nn.model import Nn
import numpy as np

# 拿到句子 段落


class Diagram(object):

    def __init__(self, config):
        self.config = config
        import matplotlib.pyplot as plt
        self.fig = plt.figure(figsize=(12, 8))
        self.plt = plt
        self.count = 0

    def start(self):
        self.plt.ion()  # 开启交互绘图
        self.axs = {}
        # 添加子图
        for i in range(self.config.subplot_num):  # 最多9张
            name = 'ax' + str(i + 1)
            self.axs[name] = self.fig.add_subplot(321 + i)

    def show(self, data):
        # 通过余数，依次顺序更新
        remainder = self.count % self.config.subplot_num
        ax_name = 'ax' + str(remainder + 1)

        self.axs[ax_name].clear()
        self.axs[ax_name].plot(data, 'b-')
        self.count += 1
        self.plt.pause(0.001)  # 显示出来

    def close(self):
        self.plt.close()


class Main(object):

    def __init__(self, config):
        self.sentence = Sentence(config)
        wv = Wv(config)
        self.db = Db(config, wv)
        self.dataset = Dataset(config, self.db)
        self.nn = Nn(config)
        self.config = config

        if self.config.env == 'development':
            self.diagram = Diagram(config)
            self.diagram.start()

    def train_sentence(self, sentence):
        word_n_context_pairs = self.sentence.getWordAndContext(sentence)
        for pair in word_n_context_pairs:
            self.train_centerword_n_context_pair(pair)

        if self.config.env == 'development':
            self.diagram.close()

    def train_centerword_n_context_pair(self, pair):
        center = pair['word']
        contexts = pair['context']
        print('training word:', center)
        for target in contexts:
            self.train_center_n_target(center, target)

    def train_center_n_target(self, center, target):
        c, t, n = self.dataset.get(center, target)  # 换取得到word vector的值
        self.nn.build(c, t, n)  # 一组center target negs
        c, t, n, cost_list = self.nn.train().export()
        self.dataset.set(c, t, n)  # 保存回去

        if self.config.env == 'development':
            self.diagram.show(cost_list)

    def save(self):
        self.db.save()


string = "我爱北京天安门测试一下是不是正确，天安门上太阳升，父流程表单匹配字段中，说明文字控件不应该出现，上传文字和上传图片、日期区间控件父表单未筛选出来"
main = Main(Config)
main.train_sentence(string)
main.save()
print(main.db.data)
