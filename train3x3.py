import logging
import coloredlogs
from AlphaZero.Coach import Coach
from AlphaZero.utils import dotdict
from AlphaZero.keras.NNetWrapper import NNetWrapper as nn

from dotsandboxes.DotsAndBoxesGame import DotsAndBoxesGame

log = logging.getLogger(__name__)

coloredlogs.install(level='INFO')  # Change this to DEBUG to see more info.

args = dotdict({
    'numIters': 30,
    'numEps': 100,  # Number of complete self-play games to simulate during a new iteration.
    'tempThreshold': 15,
    # During arena playoff, new neural net will be accepted if threshold or more of games are won.
    'updateThreshold': 0.6,
    'maxlenOfQueue': 200000,  # Number of game examples to train the neural networks.
    'numMCTSSims': 25,  # Number of games moves for MCTS to simulate.
    'arenaCompare': 40,  # Number of games to play during arena play to determine if new net will be accepted.
    'cpuct': 1,
    'checkpoint': './training/3x3',
    'load_model': True,
    'load_folder_file': ('models/3x3', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,

})

args['numIters'] = 30
args['numEps'] = 50
args['arenaCompare'] = 40


def main():
    log.info('Loading %s...', DotsAndBoxesGame.__name__)
    g = DotsAndBoxesGame(n=3)
    log.info('Loading %s...', nn.__name__)
    nnet = nn(g)
    if args.load_model:
        nnet.load_checkpoint(args.load_folder_file[0], args.load_folder_file[1])
    else:
        log.warning('Not loading a checkpoint!')
    log.info('Loading the Coach...')
    c = Coach(g, nnet, args)
    log.info('Starting the learning process 🎉')
    c.learn()


if __name__ == "__main__":
    main()
