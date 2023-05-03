import numpy as np
import Arena
from dotsandboxes.DotsAndBoxesGame import DotsAndBoxesGame
from dotsandboxes.Players import MCTSPlayer, MinimaxPlayer, AlphaZeroPlayer
from graphDataUtils import graph_data

if __name__ == '__main__':
    size = 5
    numGames = 2

    g = DotsAndBoxesGame(size)
    n1p = AlphaZeroPlayer(g, f"./models/{size}x{size}", 50)
    n2p = AlphaZeroPlayer(g, f"./models/{size}x{size}", 50)
    mmp1 = MinimaxPlayer(g, 20)
    mmp2 = MinimaxPlayer(g, 20)
    mctsp2 = MCTSPlayer(g, 500)
    mctsp1 = MCTSPlayer(g, 50)
    p1 = mmp1
    p2 = n1p
    arena = Arena.Arena(p1.play, p2.play, g, display=DotsAndBoxesGame.display_board)
    oneWon, twoWon, draws, avg_t1, avg_t2, avg_game_time, avg_margin = arena.playGames(numGames, verbose=True, log_data=True)
    print()
    print("{}: {}, {}: {}, draws: {}, ".format(p1.name, oneWon, p2.name, twoWon, draws))
    print("avgT1: {}, avgT2: {}, avgGameTime: {}".format(np.mean(avg_t1),np.mean(avg_t2),np.mean(avg_game_time)))
    print("Avg margin of victory: {}".format(np.mean(avg_margin)))
    graph_data.graphGameTime(numGames, avg_game_time)
    graph_data.graphAverageTurn(numGames, avg_t1, avg_t2, p1.name, p2.name)
    graph_data.graphMarginVictory(numGames, avg_margin)
