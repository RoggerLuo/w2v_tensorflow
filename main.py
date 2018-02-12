import numpy as np
from train.train import Train
from config import Config


class Task(object):

    def __init__(self):
        self.train = Train()

    def basic(self, string):
        for i in range(Config.repeate_times):
            cost = self.train.sentence_str(string)
            print(cost)
        self.train.save()

    def readTxtLine(self, line):
        if len(line) > 20 :
            self.basic(line)


def test():
    string = "我爱北京天安门测试一下是不是正确，天安门上太阳升，父流程表单匹配字段中，说明文字控件不应该出现，上传文字和上传图片、日期区间控件父表单未筛选出来"
    t = Task()
    t.basic(string)
