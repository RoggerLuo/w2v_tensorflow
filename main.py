from sentence import Sentence
from wv import Wv
from config import Config
from dataset import Dataset
from db import Db
from nn.model import Nn
import numpy as np

# 拿到句子 段落


class Main(object):

    def __init__(self, config):
        self.sentence = Sentence(config)
        wv = Wv(config)
        self.db = Db(config,wv)
        self.dataset = Dataset(config,self.db)
        self.nn = Nn(config)
        # self.config = config

    def train_setence(self, string):
        print('解析sentence string...')
        # context and word pairs
        word_n_context_pairs = self.sentence.getWordAndContext(string)
        for pair in word_n_context_pairs:
            center = pair['word']
            contexts = pair['context']
            for target in contexts:
                print('dataset get ...')
                c, t, n = self.dataset.get(center, target)  # 换取得到word vector的值
                print('nn build ...')
                self.nn.build(c, t, n)  # 一组center target negs
                print('nn train ...')
                c, t, n = self.nn.train().export()
                self.dataset.set(c, t, n)  # 保存回去

    def save(self):
        self.db.save()


string = "我爱北京天安门测试一下是不是正确，天安门上太阳升，父流程表单匹配字段中，说明文字控件不应该出现，上传文字和上传图片、日期区间控件父表单未筛选出来"
main = Main(Config)
main.train_setence(string)
main.save()
print(main.db.data)


