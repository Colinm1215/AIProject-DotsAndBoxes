import numpy as np
from matplotlib import pyplot as plt


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
