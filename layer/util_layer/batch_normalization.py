import tensorflow as tf

from layer.layer import Layer


class BatchNormalization(Layer):
    def __init__(self, learning_rate=None, momentum=None, axis=[0,1,2], scope="batch_normalization_layer"):
        super().__init__(trainable=True, scope=scope)
        self.epsilon = 0.0001
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.axis = axis

    def __str__(self):
        return "BatchNormalization()"

    def build_forward(self, input_vec, remember_input=True, gather_stats=False):
        with tf.variable_scope(self.scope, reuse=tf.AUTO_REUSE):
            self.save_shape(input_vec)
            if remember_input:
                self.input_vec = input_vec
            input_shape = input_vec.get_shape()[1:]

            gamma = tf.get_variable("gamma", input_shape, initializer=tf.ones_initializer())
            beta = tf.get_variable("beta", input_shape, initializer=tf.zeros_initializer())
            batch_mean, batch_var = tf.nn.moments(input_vec, self.axis)
            self.output = tf.nn.batch_normalization(input_vec, batch_mean, batch_var, beta, gamma, self.epsilon,
                                                    "batch_n")

            if gather_stats:
                tf.summary.histogram("input", input_vec, family=self.scope)
                tf.summary.histogram("mean", batch_mean, family=self.scope)
                tf.summary.histogram("var", batch_var, family=self.scope)
                tf.summary.histogram("gamma", gamma, family=self.scope)
                tf.summary.histogram("beta", beta, family=self.scope)
                tf.summary.histogram("input_normalized", self.output, family=self.scope)

            return self.output

    def build_backward(self, error, gather_stats=False):
        with tf.variable_scope(self.scope, reuse=tf.AUTO_REUSE):
            input_vec = self.restore_input()
            gamma = tf.get_variable("gamma")
            beta = tf.get_variable("beta")
            delta_gamma = tf.get_variable("delta_beta", gamma.shape, initializer=tf.zeros_initializer())
            delta_beta = tf.get_variable("delta_beta", beta.shape, initializer=tf.zeros_initializer())

            grads = tf.gradients(self.output, [input_vec, gamma, beta], error)
            delta_gamma = tf.assign(delta_gamma, grads[1] + tf.multiply(self.momentum, delta_gamma))
            delta_beta = tf.assign(delta_gamma, grads[2] + tf.multiply(self.momentum, delta_beta))

            gamma = tf.assign(gamma, tf.subtract(gamma, tf.multiply(self.learning_rate, delta_gamma)))
            beta = tf.assign(beta, tf.subtract(beta, tf.multiply(self.learning_rate, delta_beta)))
            self.step = [gamma, beta]

            if gather_stats:
                tf.summary.histogram("delta_gamma", grads[1], family=self.scope)
                tf.summary.histogram("delta_beta", grads[2], family=self.scope)
                tf.summary.histogram("output_error", grads[0], family=self.scope)

            return grads[0]
