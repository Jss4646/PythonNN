from typing import List, Any

import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Neuron:
    def __init__(self, inputs=None) -> None:
        """
        A Network Neuron

        Parameters
        ----------
        inputs : array_like
            Inputs from either the source image or a previous layer

        Examples
        --------
        >>> neuron1 = Neuron([0.24, 0.52, 0.01])

        >>> neuron2 = Neuron([0.2])

        >>> neuron3 = Neuron([1, 1, 1])

        References
        ----------
            See : http://neuralnetworksanddeeplearning.com/chap1.html#sigmoid_neurons
                  for the maths behind a Neuron
        """
        if inputs is None:
            self.inputs = []
        self.inputs = inputs
        self.weights = np.random.standard_normal(len(inputs))
        self.bias = np.random.randint(-1, 1)
        self.output = 0

    def run(self) -> float:
        """
        Takes `self.inputs` and produces an output using
        the sum of inputs * weights then adding the bias and
        passing through the sigmoid function

        Returns
        -------
        output : float
            The output of the neuron once it has been passed through
            the neuron's
        """
        for inp, weight in zip(self.inputs, self.weights):
            self.output += inp * weight

        self.output += self.bias
        self.output = sigmoid(self.output)
        return self.output


class Network:
    def __init__(self, layers: list) -> None:
        pass


