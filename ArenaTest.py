import numpy as np
import Arena
from dotsandboxes.DotsAndBoxesGame import DotsAndBoxesGame
from dotsandboxes.Players import MCTSPlayer, MinimaxPlayer, AlphaZeroPlayer
from utils import graph_data

if __name__ == '__main__':
    g = DotsAndBoxesGame(3)

    n1p = AlphaZeroPlayer(g, "./models/3x3", 50)
    mmp1 = MinimaxPlayer(g, 8)
    mctsp2 = MCTSPlayer(g, 500)
    mctsp1 = MCTSPlayer(g, 500)
    mmp2 = MinimaxPlayer(g, 8)
    n2p = AlphaZeroPlayer(g, "./models/3x3", 50)

    p2 = n2p
    p1 = n1p

    numGames = 40

    arena = Arena.Arena(p1.play, p2.play, g, display=DotsAndBoxesGame.display_board)
    oneWon, twoWon, draws, avg_t1, avg_t2, avg_game_time, avg_margin = arena.playGames(numGames, verbose=False, log_data=True)
    print()
    print("{}: {}, {}: {}, draws: {}, ".format(p1.name, oneWon, p2.name, twoWon, draws))
    print("avgT1: {}, avgT2: {}, avgGameTime: {}".format(np.mean(avg_t1),np.mean(avg_t2) ,np.mean(avg_game_time)))
    print("Avg margin of victory: {}".format(np.mean(avg_margin)))
    graph_data.graphGameTime(numGames, avg_game_time)
    graph_data.graphAverageTurn(numGames, avg_t1, avg_t2, p1.name, p2.name)
