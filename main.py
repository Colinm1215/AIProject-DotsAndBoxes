import numpy as np
from Arena import Arena
from DotsAndBoxes.DotsAndBoxesGame import DotsAndBoxesGame as db
from DotsAndBoxes.Players import MinimaxPlayer, MCTSPlayer, HumanPlayer, AlphaZeroPlayer


def getPlayerType(game, player_num):
    player_type = 0
    player = None
    while player_type == 0:
        player_type = int(input(f"Please enter player {player_num}'s play type\n"
                                "1.) manual\n"
                                "2.) minimax\n"
                                "3.) mcts\n"
                                "4.) alphaZero\n"))
        if player_type == 1:
            player = HumanPlayer(game, 0)
        elif player_type == 2:
            depth = int(input("At what max_depth should the minimax algorithm search to find a move? : "))
            player = MinimaxPlayer(game, depth)
        elif player_type == 3:
            sims = int(input("How many simulations should MCTS use to find a move? : "))
            player = MCTSPlayer(game, sims)
        elif player_type == 4:
            sims = int(input("How many simulations should AlphaZero's MCTS use?: "))
            player = AlphaZeroPlayer(game, f"./models/{size}x{size}", sims)
        else:
            print("Invalid Type")
            player_type = 0
    return player


# The program begins by allowing the user to choose from a scenario gamestate or select a new gamestate (a new game).
# If a scenario is given, the user inputs the current turn for the given scenario.
# If a new game is selected, the user enters the board size.
# Finally, the user selects the max_depth the MiniMax algorithm should use during move selection.
# The game is then played out between two AI players.
# The game board is printed after each turn.
# The board is evaluated after each turn to determine if it is over. If so, a result is displayed.
# The time of each turn and overall game is tracked.
if __name__ == '__main__':
    size = 0
    while size == 0:
        size = int(input("Enter game board size (3 or 5): "))
        if not (size == 3 or size == 5):
            print("Invalid Size")
            size = 0

    game = db(size)
    p1 = getPlayerType(game, 1)
    p2 = getPlayerType(game, 2)

    numGames = int(input("How many games should be simulated?: "))
    arena = Arena(p1.play, p2.play, game, display=game.display_board)
    oneWon, twoWon, draws, avg_t1, avg_t2, avg_game_time, avg_margin = arena.playGames(numGames, verbose=True,
                                                                                       log_data=True)
    print()
    print("{}: {}, {}: {}, draws: {}, ".format(p1.name, oneWon, p2.name, twoWon, draws))
    print("avgT1: {}, avgT2: {}, avgGameTime: {}".format(np.mean(avg_t1), np.mean(avg_t2), np.mean(avg_game_time)))
