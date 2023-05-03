import matplotlib
import numpy as np
import matplotlib.pyplot as plt


class AverageMeter(object):
    """From https://github.com/pytorch/examples/blob/master/imagenet/main.py"""

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def __repr__(self):
        return f'{self.avg:.2e}'

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


class dotdict(dict):
    def __getattr__(self, name):
        return self[name]


class graph_data:
    @staticmethod
    def graphGameTime(num_games, data_points):
        x = np.arange(1, num_games + 1)
        y = data_points
        plt.bar(x, y)
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
        plt.xlabel("Game")
        plt.ylabel("Average Time")
        plt.title("Average Game Time (seconds)")
        plt.show()

    @staticmethod
    def graphMarginVictory(num_games, data_points):
        x = np.arange(1, num_games + 1)
        y = data_points
        plt.bar(x, y)
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
        plt.xlabel("Game")
        plt.ylabel("Margin of Victory")
        plt.title("Average Margin of Victory")
        plt.show()

    @staticmethod
    def graphAverageTurn(num_games, t1, t2, name1, name2):
        x = np.arange(1, num_games + 1)
        y1 = t1
        y2 = t2
        plt.plot(x, y1, label=name1, linewidth='3')
        plt.plot(x, y2, label=name2, linewidth='3')
        plt.xticks(np.arange(min(x), max(x) + 1, 1.0))
        plt.xlabel("Game")
        plt.ylabel("Average Time")
        plt.title("Average Turn Time (seconds)")
        plt.xlim(left=1, right=num_games)
        plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.show()

