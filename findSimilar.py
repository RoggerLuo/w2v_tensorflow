from train.dataset.db import Db
from train.config import Config
import numpy as np


def findWord(db, word, length=10):
    entrys = db.getEntrysByWord(word)
    if len(entrys) == 0:
        print('没找到')
        return False
    
    entry = entrys[0]
    
    unsortedList = []
    for et in db.data:
        deviationArr = entry['vec'][:8] - et['vec'][:8]
        # deviationArr = np.fabs(deviationArr)
        deviationArr = [round(de, 5) for de in deviationArr.tolist()]
        deviationArr = np.square(np.array(deviationArr))
        # deviationArr = np.array(deviationArr)
        deviation = np.sum(deviationArr)
        unsortedList.append({'deviation': deviation, 'word': et['word']})

    sortedList = sorted(unsortedList, key=lambda dic: dic['deviation'])

    for element in sortedList[0:length]:
        print(element['word'])

db = Db(Config)
findWord(db,'嫉妒', 20)
