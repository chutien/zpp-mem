import tensorflow as tf

from layer.weight_layer.weight_layer import WeightLayer


class FullyConnected(WeightLayer):
    def __init__(self, output_dim, func=(lambda x, w : tf.matmul(x, w)),
                 weights_initializer=tf.initializers.he_normal, flatten=False, add_biases=True,
                 biases_initializer=tf.zeros_initializer, scope="fully_connected_layer"):
        super().__init__(func, scope)
        self.output_dim = output_dim
        self.func = func
        self.weights_initializer = weights_initializer
        self.flatten = flatten
        self.add_biases = add_biases
        self.biases_initializer = biases_initializer

    def __str__(self):
        return f"FullyConnected({self.output_dim})"
    
    def gather_stats_backward(self, gradients):
        weights = self.variables[0]
        tf.summary.image(f"weights_{self.scope}", tf.reshape(weights, (1, weights.shape[0], weights.shape[1], 1)))

    def build_forward(self, input, remember_input=False, gather_stats=False):
        if remember_input:
            self.save_input(input)
        with tf.variable_scope(self.scope, reuse=tf.AUTO_REUSE):
            if self.flatten:
                input = tf.layers.flatten(input)
            weights = tf.get_variable("weights", [input.shape[1], self.output_dim],
                                      initializer=self.weights_initializer())
            self.variables.append(weights)
            output = self.func(input, weights)
            if self.add_biases:
                biases = tf.get_variable("biases", [self.output_dim],
                                         initializer=self.biases_initializer())
                self.variables.append(biases)
                output = tf.add(output, biases)
            return output
