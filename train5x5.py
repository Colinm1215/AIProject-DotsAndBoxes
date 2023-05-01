import logging
import coloredlogs
from Coach import Coach
from utils import dotdict
from DotsAndBoxes.keras.NNetWrapper import NNetWrapper as nn

from DotsAndBoxes.DotsAndBoxesGame import DotsAndBoxesGame

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
    'checkpoint': './training/5x5/',
    'load_model': False,
    'load_folder_file': ('models/5x5', 'best.pth.tar'),
    'numItersForTrainExamplesHistory': 20,
})

args['numIters'] = 20
args['numEps'] = 30
args['arenaCompare'] = 40


def main():
    log.info('Loading %s...', DotsAndBoxesGame.__name__)
    g = DotsAndBoxesGame(n=5)
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
