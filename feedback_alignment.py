from backward_propagation import BackwardPropagation
from propagator import FixedRandom


class FeedbackAlignment(BackwardPropagation):
    def __init__(self, types, shapes, sequence, propagator=FixedRandom(), *args, **kwargs):
            super().__init__(types, shapes, sequence, propagator, *args, **kwargs)
