import numpy as np


class Dataset(object):

    def __init__(self, config, db):
        self.config = config
        self.db = db

    def get_negSamples(self):
        total_num = len(self.db.data)
        max_value = total_num - 1
        if max_value <= 0: return []

        # 如果可以选择的neg 还不够 要求的，那么，调整要求为最大可获得的neg_num
        neg_sample_num = self.config.neg_sample_num
        available_neg_num = total_num - 2
        if available_neg_num < self.config.neg_sample_num:
            neg_sample_num = available_neg_num

        negSamples = []
        while len(negSamples) < neg_sample_num - 1:
            randomEntry = self.db.data[np.random.randint(total_num)]
            if randomEntry['word'] != self.center['word']:
                if randomEntry['word'] != self.target['word']:
                    negSamples.append(randomEntry)
        return negSamples

    def get(self, center, target):  # TrainingPairs
        self.center = self.db.getEntryByWord(center)
        self.target = self.db.getEntryByWord(target)
        self.negSamples = self.get_negSamples()

        length = self.config.vector_dimsensions

        negs = [neg['vec'][length:] for neg in self.negSamples] # 后一半vector
        return self.center['vec'][:length], self.target['vec'][length:], negs # 前一半 后一半

    def set(self, center, target, negSamples):
        length = self.config.vector_dimsensions
        self.center['vec'][:length] = center
        self.target['vec'][length:] = target
        for ind in range(len(negSamples)):
            self.negSamples[ind]['vec'][length:] = negSamples[ind]


# center = np.array([1, 2, 3])
# target = np.array([4, 5, 6])
# negs = [np.array([7, 8, 9]), np.array([3, 6, 9])]


# 测试是否更新到了db，不需要traing 直接给值
# def test():
    # from config import Config
    # string = "我爱北京天安门测试一下是不是正确，天安门上太阳升，父流程表单匹配字段中，说明文字控件不应该出现，上传文字和上传图片、日期区间控件父表单未筛选出来"

# 测试getNegSamples


# def test2():

# test()
