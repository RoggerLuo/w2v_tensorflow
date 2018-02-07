import numpy as np

center = np.array([1, 2, 3])
target = np.array([4, 5, 6])
negs = [np.array([7, 8, 9]), np.array([3, 6, 9])]


class Dataset(object):

    def __init__(self, config):
        self.config = config

    def prepare(self,centerword,targetword):

    
    def getNegSamples(self,word_pair):

    def get(self,word_pair): # TrainingPairs
        
    def set(self,)

def test():
    class Config(object):
        vector_dimsensions = 2

test()

def main():
    string = from_db_or_from_somewhere()

    sentence = Sentence(Config)
    dataset = Dataset(Config)
    db = Db(Config)
    
    word_n_context_pairs = sentence.getWordAndContext(string)
    for pair in word_n_context_pairs:
        center = pair['word']
        contexts = pair['context']
        for target in contexts:
            nn.build(dataset.get(center,target)) # 一组cen target negs
            nn.train()
            dataset.set(nn.export())


    db.save()



