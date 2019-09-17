from typing import List, Any

import numpy as np


def sigmoid(x) -> float:
    return 1 / (1 + np.exp(-x))


def relu(x) -> float:
    return np.maximum(x, 0)


class Neuron:
    """
    A Network Neuron

    Parameters
    ----------
    num_of_inputs : int
        Inputs from either the source image or a previous layer

    activation_function : str
        Tells the node what activation type to use
        Supported activation types:
            -Sigmoid
            -ReLU

    Examples
    --------
    >>> neuron1 = Neuron(4)
    >>> neuron2 = Neuron(10, 'sigmoid')
    >>> neuron3 = Neuron(2, 'relu')

    References
    ----------
        See : http://neuralnetworksanddeeplearning.com/chap1.html#sigmoid_neurons
              for the maths behind a Neuron
    """
    def __init__(self, num_of_inputs: int, activation_function='sigmoid'):
        self.weights = np.random.standard_normal(num_of_inputs)
        self.bias = np.random.randint(-1, 1)
        self.output = 0

        if activation_function.lower() == 'sigmoid':
            self.activation_function = sigmoid
        elif activation_function.lower() == 'relu':
            self.activation_function = relu
        else:
            raise ValueError(f'\n{activation_function} is not supported.'
                             f'\nHere are a list of supported functions:'
                             f'\n\t-sigmoid'
                             f'\n\t-relu')

    def run(self, inputs: list) -> float:
        """
        Takes `self.inputs` and produces an output using
        the sum of inputs * weights then adding the bias and
        passing through the sigmoid function

        Parameters
        ----------
        inputs : array_like
            Inputs from either the source image or a previous layer

        Returns
        -------
        output : float
            The output of the neuron once it has been passed through
            the neuron's
        """
        for inp, weight in zip(inputs, self.weights):
            self.output += inp * weight

        self.output += self.bias
        self.output = self.activation_function(self.output)
        return self.output


class Network:
    # TODO add documentation
    def __init__(self, data_set: list, layers: dict) -> None:

        self.layers = []
        self.data_set = data_set

        for index, layer in enumerate(layers.values()):
            activation = layer['activation']
            num_of_neurons = layer['neurons']

            if index == 0:
                self.layers.append([Neuron(len(data_set), activation) for num in range(num_of_neurons)])
            else:
                self.layers.append([Neuron(prev_num_of_neurons, activation) for num in range(num_of_neurons)])

            prev_num_of_neurons = num_of_neurons


data_set = [0.2]

layers = {
    'layer 1': {
        'activation': 'relu',
        'neurons': 10,
    },
    'layer 2': {
        'activation': 'sigmoid',
        'neurons': 20,
    },
    'Layer 3': {
        'activation': 'sigmoid',
        'neurons': 10,
    },
}

network = Network(data_set, layers)
print(network.layers)
print(network.layers[0][0])
