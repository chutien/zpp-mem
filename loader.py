import tensorflow as tf


def load(dataset_name):
    if dataset_name is 'mnist':
        return load_mnist()


def load_mnist():
    training, test = tf.keras.datasets.mnist.load_data()

    def transform(feature, label):
        feature = tf.reshape(feature, [-1])
        label = tf.one_hot(label, 10)
        feature = tf.to_float(feature) / 255.0
        return feature, label

    train_data_set = tf.data.Dataset.from_tensor_slices(training).map(transform).batch(1)
    test_data_set = tf.data.Dataset.from_tensor_slices(test).map(transform).batch(1)

    return train_data_set, test_data_set
