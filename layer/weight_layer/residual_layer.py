import tensorflow as tf

from layer.weight_layer.convolutional_layers import ConvolutionalLayer
from layer.weight_layer.weight_layer import WeightLayer


class ResidualLayer(WeightLayer):
    def __init__(self, sequence, trainable=True, learning_rate=None, momentum=None, scope="residual_layer"):
        super().__init__(trainable, scope=scope)
        self.propagator = None
        self.sequence = sequence
        self.shortcut_conv = None
        self.learning_rate = learning_rate
        self.momentum = momentum


    def __str__(self):
        s = f"ResidualLayer["
        for layer in self.sequence:
            s = s + f", {str(layer)}"
        s = s + "]"
        return s

    def build_forward(self, input, remember_input=False, gather_stats=False):
        if remember_input:
            self.input = input

        with tf.variable_scope(self.scope, tf.AUTO_REUSE):
            for i, layer in enumerate(self.sequence):
                layer.scope = f"{self.scope}_{i}_{layer.scope}"
                layer.set_lr(self.learning_rate)
                layer.set_momentum(self.momentum)
                if isinstance(layer, WeightLayer):
                    layer.propagator = self.propagator

            residual = input
            for layer in self.sequence:
                residual = layer.build_forward(residual, remember_input=True, gather_stats=gather_stats)

            res_shape = residual.shape
            input_shape = input.shape

            stride_width = int(round(input_shape[1].value / res_shape[1].value))
            stride_height = int(round(input_shape[2].value / res_shape[2].value))

            equal_channels = input_shape[3].value == res_shape[3].value
            if stride_width > 1 or stride_height > 1 or not equal_channels:
                self.shortcut_conv = ConvolutionalLayer(number_of_filters=res_shape[3],
                                  filter_dim=(1, 1),
                                  stride=[stride_width, stride_height],
                                  padding="VALID",
                                  learning_rate=self.learning_rate,
                                  scope=f"{self.scope}_{len(self.sequence)}_shortcut_convolution")
                self.shortcut_conv.propagator = self.propagator
                input = self.shortcut_conv.build_forward(input)

            return input + residual

    def build_backward(self, error, gather_stats=False):
        input_err = 1
        self.step = []
        with tf.variable_scope(self.scope, tf.AUTO_REUSE):
            if self.shortcut_conv is not None:
                input_err = self.shortcut_conv.build_backward(error, gather_stats=gather_stats)
                self.step.append(self.shortcut_conv.step)
            for layer in reversed(self.sequence):
                error = layer.build_backward(error, gather_stats=gather_stats)
                if layer.trainable:
                    self.step.append(layer.step)

            return error + input_err

    def build_propagate(self, error, gather_stats=False):
        pass

    def build_update(self, error, gather_stats=False):
        pass
