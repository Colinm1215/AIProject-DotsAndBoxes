import unittest
from Arena import Arena
from DotsAndBoxes import DotsAndBoxesGame
from DotsAndBoxes.Players import RandomPlayer, AlphaZeroPlayer


class TestDotsAndBoxes(unittest.TestCase):

    @staticmethod
    def test_game_run():
        g = DotsAndBoxesGame.DotsAndBoxesGame(3)
        rp = RandomPlayer(g).play
        n1p = AlphaZeroPlayer(g, './models/3x3', 25)

        arena = Arena(rp, n1p.play, g, display=DotsAndBoxesGame.DotsAndBoxesGame.display_board)
        print(arena.playGames(2, verbose=False))


if __name__ == '__main__':
    unittest.main()
