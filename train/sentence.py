import jieba
import numpy as np

ignoreds = ['，', ',', '的', '是', '\n', ' ', '(', ')', '.', '/']


class Sentence(object):

    def __init__(self, config):
        self.config = config
        self.word_list = []

    def segment(self):
        self.word_list = jieba.lcut(self.string)  # 默认是精确模式

    def filter(self):
        filtered_list = []
        for word in self.word_list:
            if word not in ignoreds:
                filtered_list.append(word)
        self.word_list = filtered_list

    def getWordAndContext(self, string):
        self.string = string
        self.segment()
        self.filter()
        word_n_context_pairs = []
        c = self.config.window_size
        for index in range(len(self.word_list)):
            # 滑窗的start\end\index
            word = self.word_list[index]
            start = index - c if (index - c) >= 0 else 0
            end = index + 1 + \
                c if (index + 1 + c) <= len(self.word_list) else len(self.word_list)

            context = self.word_list[start:index]  # 选中的词之前的
            context2 = self.word_list[index + 1:end]  # 选中的词之后的
            context.extend(context2)

            # 用一个tuple表示
            item = {'word': word, 'context': context}
            word_n_context_pairs.append(item)
        return word_n_context_pairs


def test():
    class Config(object):
        vector_dimsensions = 8
        window_size = 3
    s = Sentence(Config)
    [print(item['word'], item['context'])
     for item in s.getWordAndContext("我爱北京天安门测试一下是不是正确，天安门上太阳升")]

# test()
