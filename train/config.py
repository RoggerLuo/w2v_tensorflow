
class Config(object):
    db_path = './w2v.pkl'
    vector_dimsensions = 8
    neg_sample_num = 10
    window_size = 3
    # training nn
    # env = 'development'
    env = 'production'
    # repeate_times = 5
    learning_rate = 0.05
    
    subplot_num = 9
    subplot_structrue = 331 # 从331或者321开始
