import unittest

import numpy as np
import Arena
from dotsandboxes.DotsAndBoxesGame import DotsAndBoxesGame as db
from dotsandboxes.Players import RandomPlayer, AlphaZeroPlayer, MinimaxPlayer, MCTSPlayer
from AlphaZero.keras.NNetWrapper import NNetWrapper

scenarios3x3 = [['scenario1-3.1-matrix.txt', 8],
                ['scenario2-3.2-matrix.txt', 9],
                ['scenario3-3.3-matrix.txt', 3],
                ['scenario4-3.4-matrix.txt', 18],
                ['scenario5-3.5-matrix.txt', 0],
                ['scenario6-3.6-matrix.txt', 16]]


class TestDotsAndBoxes(unittest.TestCase):

    def test_game_run(self):
        g = db(3)
        rp = RandomPlayer(g).play
        n1p = AlphaZeroPlayer(g, '../models/3x3', 25)

        arena = Arena(rp, n1p.play, g, display=db.display_board)
        print(arena.playGames(2, verbose=False))

    def test_model_sum(self):
        game = db(3)
        n1 = NNetWrapper(game)
        print(n1.nnet.model.summary())
        print("")

    def test_scenarios3x3Minimax(self):
        print("Testing Minimax 3x3")
        play_scenarios_minimax(3, scenarios3x3)
        print("")

    def test_scenarios3x3MCTS(self):
        print("Testing MCTS 3x3")
        play_scenarios_MCTS(3, scenarios3x3)
        print("")

    def test_scenarios3x3AlphaZero(self):
        print("Testing Alpha Zero 3x3")
        play_scenarios_AlphaZero(3, scenarios3x3)
        print("")


def play_scenarios_MCTS(size, scenarios, sims=500):
    g = db(size)
    mcts1 = MCTSPlayer(g, sims)
    testScenarios(g, scenarios, mcts1)


def play_scenarios_minimax(size, scenarios, depth=40):
    g = db(size)
    mmp1 = MinimaxPlayer(g, depth)
    testScenarios(g, scenarios, mmp1)


def play_scenarios_AlphaZero(size, scenarios, sims=50):
    g = db(size)
    n1p = AlphaZeroPlayer(g, f'./models/{size}x{size}', sims)
    testScenarios(g, scenarios, n1p)


def testScenarios(game, scenarios, agent, test_num=10):
    for scenario in scenarios:
        print(f'Testing scenario: {scenario[0]}')
        board = game.read_gamestate(f'./scenarios/{scenario[0]}')
        count = 0
        a_list = []
        for i in range(test_num):
            action = agent.play(np.copy(board))
            a_list.append(action)
            if action == scenario[1]:
                count += 1
        print(f'Action List: {a_list}')
        print(f'Correct Plays: {count} out of {test_num}\n')
    print("")


if __name__ == '__main__':
    unittest.main()
