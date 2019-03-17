import tensorflow as tf


def load_cifar100():
    training, test = tf.keras.datasets.cifar100.load_data()

    def transform(feature, label):
        feature = tf.reshape(feature, [32,32,3])
        label = label[0]
        label = tf.one_hot(label, 100)
        feature = tf.to_float(feature) / 255.0
        return feature, label

    train_data_set = tf.data.Dataset.from_tensor_slices(training).map(transform)
    test_data_set = tf.data.Dataset.from_tensor_slices(test).map(transform)

    return train_data_set, test_data_set


def load_cifar10():
    training, test = tf.keras.datasets.cifar10.load_data()

    def transform(feature, label):
        feature = tf.reshape(feature, [32,32,3])
        label = label[0]
        label = tf.one_hot(label, 10)
        feature = tf.to_float(feature) / 255.0
        return feature, label

    train_data_set = tf.data.Dataset.from_tensor_slices(training).map(transform)
    test_data_set = tf.data.Dataset.from_tensor_slices(test).map(transform)

    return train_data_set, test_data_set


def load_mnist():
    training, test = tf.keras.datasets.mnist.load_data()

    def transform(feature, label):
        feature = tf.reshape(feature, [28, 28, 1])
        label = tf.one_hot(label, 10)
        feature = tf.to_float(feature) / 255.0
        return feature, label

    train_data_set = tf.data.Dataset.from_tensor_slices(training).map(transform)
    test_data_set = tf.data.Dataset.from_tensor_slices(test).map(transform)

    return train_data_set, test_data_set


datasets = {
    "mnist": load_mnist,
    "cifar100": load_cifar100,
    "cifar10": load_cifar10
}
