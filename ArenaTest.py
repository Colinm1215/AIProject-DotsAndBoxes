import numpy as np

import Arena
from MCTS import MCTS
from DotsAndBoxes import DotsAndBoxesGame
from Players import HumanPlayer, MCTSPlayer, MinimaxPlayer
from NNetWrap import NNetWrapper
from utils import dotdict
import os

if __name__ == '__main__':
    g = DotsAndBoxesGame(3)

    numMCTSSims = 50
    n1 = NNetWrapper(g)
    n1.load_checkpoint(os.path.join('./temp'), 'best.pth.tar')
    args1 = dotdict({'numMCTSSims': numMCTSSims, 'cpuct': 1.0})
    mcts1 = MCTS(g, n1, args1)
    n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))

    mmp1 = MinimaxPlayer(g, 6).play
    mctsp2 = MCTSPlayer(g, 3000).play

    p1 = mmp1
    p2 = mctsp2

    arena = Arena.Arena(p1, p2, g, display=DotsAndBoxesGame.dispDummy)
    oneWon, twoWon, draws = arena.playGames(40, verbose=False)
    print("oneWon: {}, twoWon: {}, draws: {}".format(oneWon, twoWon, draws))
