import argparse
import time
import tensorflow as tf
from inspect import getmembers, isfunction
from definition import sequence_definitions
from definition import dataset_definitions
from definition import network_definitions


sequences_dict = dict(getmembers(sequence_definitions, isfunction))
datasets_dict = dict(getmembers(dataset_definitions, isfunction))
networks_dict = {
    network_name: network_definition for network_name, network_definition in getmembers(network_definitions)
    if isinstance(network_definition, dict) and network_name != "__builtins__"
}
networks_list = [
    network_definition for network_name, network_definition in getmembers(network_definitions)
    if isinstance(network_definition, dict) and network_name != "__builtins__"
]


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def get_id_and_name_from_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', type=int, help='number of network')
    parser.add_argument('--name', type=str, help='network name')

    parser.add_argument('--type', type=str, help='type')
    parser.add_argument('--learning_rate', type=float, help='learning rate')
    parser.add_argument('--batch_size', type=int, help='batch size')
    parser.add_argument('--epochs', type=int, help='epochs')
    parser.add_argument('--cost_function', type=str, help='cost function')
    parser.add_argument('--dataset_name', type=str, help='dataset name')
    parser.add_argument('--sequence', type=str, help='sequence')
    parser.add_argument('--seed', type=int, help='seed')
    parser.add_argument('--memory_only', type=str2bool, help='memory only')
    parser.add_argument('--gather_stats', type=str2bool, help='gather stats')
    parser.add_argument('--save_graph', type=str2bool, help='save graph')
    parser.add_argument('--minimize_manually', type=str2bool, help='minimize manually')

    
#    parser.add_argument('-momentum', type=float, help='momentum')

    network_id = parser.parse_args().id
    network_name = parser.parse_args().name
    return network_id, network_name, parser


def get_network_definition():
    network_id, network_name, parser = get_id_and_name_from_arguments()

    type = parser.parse_args().type
    learning_rate = parser.parse_args().learning_rate
    batch_size = parser.parse_args().batch_size
    epochs = parser.parse_args().epochs
    cost_function = parser.parse_args().cost_function
    dataset_name = parser.parse_args().dataset_name
    sequence = parser.parse_args().sequence
    gather_stats = parser.parse_args().gather_stats
    memory_only = parser.parse_args().memory_only
    save_graph = parser.parse_args().save_graph
    minimize_manually = parser.parse_args().minimize_manually
    seed = parser.parse_args().seed
#    momentum = parser.parse_args().momentum

    if network_id is not None:
        print(f"running network with id={network_id}")
        network_definition = dict(networks_list[network_id])
    elif network_name is not None:
        print(f"running network with name={network_name}")
        network_definition = dict(networks_dict[network_name])
    else:
        network_name = "default_network"
        network_definition = dict(networks_dict[network_name])

    if type is not None:
        network_definition.update({"type": type})
    if learning_rate is not None:
        network_definition.update({"learning_rate": learning_rate})
    if batch_size is not None:
        network_definition.update({"batch_size": batch_size})
    if epochs is not None:
        network_definition.update({"epochs": epochs})
    if cost_function is not None:
        network_definition.update({"cost_function": cost_function})
    if dataset_name is not None:
        network_definition.update({"dataset_name": dataset_name})
    if sequence is not None:
        network_definition.update({"sequence": sequence})
    if gather_stats is not None:
        network_definition.update({"gather_stats": gather_stats})
    if memory_only is not None:
        network_definition.update({"memory_only": memory_only})
    if save_graph is not None:
        network_definition.update({"save_graph": save_graph})
    if minimize_manually is not None:
        network_definition.update({"minimize_manually": minimize_manually})
    if seed is not None:
        network_definition.update({"seed": seed})
        #    if momentum is not None:
        #        network_definition.update({"momentum": momentum})
    print(network_definition)
    return network_definition


def create_network(network_definition, output_types, output_shapes):
    model = network_definition['type']
    if model == 'BP':
        from neural_network.backpropagation import Backpropagation as Network
    elif model == 'DFA':
        from neural_network.direct_feedback_alignment import DirectFeedbackAlignment as Network
    elif model == 'DFAMEM':
        from neural_network.direct_feedback_alignment import DirectFeedbackAlignmentMem as Network
    elif model == 'FA':
        from neural_network.feedback_alignment import FeedbackAlignment as Network
    else:
        raise NotImplementedError(f"Model {model} is not recognized.")

    cost_func_name = network_definition['cost_function']
    if cost_func_name == 'mean_squared_error':
        cost_func = tf.losses.mean_squared_error
    elif cost_func_name == 'sigmoid_cross_entropy':
        cost_func = tf.losses.sigmoid_cross_entropy # Do not use any activation in last layer.
    elif cost_func_name == 'softmax_cross_entropy':
        cost_func = tf.losses.softmax_cross_entropy # Do not use any activation in last layer.

    sequence = sequences_dict[network_definition['sequence']](output_shapes[1][1].value)

    return Network(output_types,
                   output_shapes,
                   sequence,
                   cost_func,
                   tf.train.GradientDescentOptimizer(network_definition["learning_rate"]),
                   scope=model,
                   gather_stats=network_definition['gather_stats'],
                   save_graph=network_definition['save_graph'],
                   restore_model_path=network_definition['restore_model_path'],
                   save_model_path=network_definition['save_model_path'],
                   restore_model=network_definition['restore_model'],
                   save_model=network_definition['save_model'],
                   minimize_manually=network_definition['minimize_manually'])


def train_network(neural_network, training, test, network):
    start_learning_time = time.time()
    neural_network.train(training_set=training,
                         validation_set=test,
                         epochs=network['epochs'],
                         eval_period=network['eval_period'],
                         stat_period=network['stat_period'],
                         memory_only=network['memory_only'],
                         minimum_accuracy=network['minimum_accuracy'])
    print(f"learning process took {time.time() - start_learning_time} seconds (realtime)")


if __name__ == '__main__':
    network_def = get_network_definition()
    if network_def['seed'] is not None:
        tf.set_random_seed(network_def['seed'])

    training_set, test_set = datasets_dict[network_def['dataset_name']](network_def['batch_size'])
    neural_net = create_network(network_def, training_set.output_types, training_set.output_shapes)
    train_network(neural_net, training_set, test_set, network_def)
