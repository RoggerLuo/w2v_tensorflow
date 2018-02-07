import numpy as np

center = np.array([1, 2, 3])
target = np.array([4, 5, 6])
negs = [np.array([7, 8, 9]), np.array([3, 6, 9])]

class Wv(object):

    def __init__(self, config):
        self.config = config

    def getStartVector(self):
        randomVec = (np.random.rand(self.config.vector_dimsensions) - 0.5)
        zerosVector = np.zeros((self.config.vector_dimsensions))
        return np.concatenate((randomVec / self.config.vector_dimsensions, zerosVector), axis=0)

def test():
    class Config(object):
        vector_dimsensions = 2
    wv = Wv(Config)
    print(wv.getStartVector())

# test()

def segment(string):
    seg_list = jieba.lcut(string)  # 默认是精确模式
    # print('||||||||||||||分词|||||||||||||')
    return seg_list


def filterWord(arr):
    # print('||||||||||||||筛选过滤|||||||||||||')
    filteredArr = []
    for word in arr:
        if word not in ignoreds:
            filteredArr.append(word)
    # print(filteredArr)
    return filteredArr


def getIdAndVector(word):
    entrys = voca_model.getWordEntrys(word)
    if len(entrys) == 0:
        startVector = np.array(getStartVector())
        insert_id = voca_model.insertVocabulary(word, startVector)
        return insert_id, startVector
    else:
        vectorFetched = entrys[0]['vector']
        vectorFetched = vectorFetched  # json.loads(vectorFetched)
        entry_id = entrys[0]['id']
        return entry_id, vectorFetched


def getDataset(string, windowLength=10):
    # segment
    wordList = segment(string)
    # filter
    arr = filterWord(wordList)

    tokens = {}
    trainingPairs = []
    wordVectors = {}
    c = windowLength

    for index in range(len(arr)):
        # 滑窗的start\end\index
        word = arr[index]
        start = index - c if (index - c) >= 0 else 0
        end = index + 1 + c if (index + 1 + c) <= len(arr) else len(arr)

        content = arr[start:index]  # 选中的词之前的
        content2 = arr[index + 1:end]  # 选中的词之后的
        content.extend(content2)
        # 用一个tuple表示
        item = (word, content)
        trainingPairs.append(item)
        # -------
        insert_id, vec = getIdAndVector(word)
        tokens[word] = insert_id
        wordVectors[word] = vec
    return trainingPairs, tokens, wordVectors


# entry = db_model.fetch_entry_untreated()
# ps, tks, vec = getDataset(entry[2], 3)
# db_model.mark_entry_as_treated(entry[0])
# print(ps)
# print(tks)
# print(vec)


# # content = getUntreatedEntry_byVersion()
# # wordList = segment(content[2])
# # wordList = filterWord(wordList)
# # test = slide(wordList,5)
# # print(test[2])
