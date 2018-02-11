import numpy as np

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
            self.axs[name] = self.fig.add_subplot(self.config.subplot_structrue + i)

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

