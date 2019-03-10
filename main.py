import argparse

from layer import *
from options import parse
from loader import load


def load_dataset(options):
    dataset = options['datasets']
    if dataset is None:
        raise RuntimeError("need dataset")
    return load(dataset['name'])


def define_network(options):
    model = options['type']
    if model == 'BP':
        from backpropagation import Backpropagation as Network
    elif model == 'DFA':
        from direct_feedback_alignment import DirectFeedbackAlignment as Network
    elif model == 'FA':
        from feedback_alignment import FeedbackAlignment as Network
    else:
        raise NotImplementedError(f"Model {model} is not recognized.")

    return Network(784,
                   [Block([FullyConnected(50), BatchNormalization(), Sigmoid()]),
                    Block([FullyConnected(30), BatchNormalization(), Sigmoid()]),
                    Block([FullyConnected(10), Sigmoid()])],
                   10,
                   learning_rate=options['training_parameters']['learning_rate'],
                   scope=options['type'],
                   gather_stats=options['training_parameters']['gather_stats'],
                   restore_model=options['model_handling']['restore'],
                   save_model=options['model_handling']['should_save'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-opt', type=str, required=True, help='Path to option JSON file.')
    opt = parse(parser.parse_args().opt)
    print(opt['aalal'])

    training, test = load_dataset(opt)
    batch_size = opt['datasets']['batch_size']
    epochs = opt['datasets']['epochs']
    eval_period = opt['periods']['eval_period']
    stat_period = opt['periods']['stat_period']

    NN = define_network(opt)
    if opt['is_train']:
        NN.train(training, test, batch_size=batch_size, epochs=epochs, eval_period=eval_period,
                 stat_period=stat_period)
    else:
        NN.test(test, batch_size)
