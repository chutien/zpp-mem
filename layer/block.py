from layer.weight_layer.weight_layer import WeightLayer
from layer.layer import Layer


class Block(object):
    def __init__(self, sequence):
        if not all(isinstance(item, Layer) for item in sequence):
            raise TypeError("All elements of sequence must be instances of layer")
        if not isinstance(sequence[0], WeightLayer):
            raise TypeError("The first element of sequence must be an instance of WeightLayer")
        self.head = sequence[0]
        self.tail = sequence[1:]

    def __len__(self):
        return len(self.tail) + 1

    def __getitem__(self, i):
        l = self.__len__()
        if abs(i) >= l:
            raise IndexError("Block index out of range")
        if i < 0:
            i += l
        if i == 0:
            return self.head
        return self.tail[i - 1]

    def __iter__(self):
        yield self.head
        for sublayer in self.tail:
            yield sublayer

    def __str__(self):
        s = f"Block[{str(self.head)}"
        for layer in self.tail:
            s = s + f", {str(layer)}"
        s = s + "]"
        return s
