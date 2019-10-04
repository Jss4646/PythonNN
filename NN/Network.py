from typing import List, Any

import numpy as np


def sigmoid(x, derivative=False) -> float:
    sigm = 1 / (1 + np.exp(-x))
    if derivative:
        return sigm * (1 - sigm)
    return sigm


def relu(x, derivative=False) -> float:
    if derivative:
        x = 0 if x < 0 else 1
        return x
    return np.maximum(x, 0)


class Neuron:
    """
    A Network Neuron

    Parameters
    ----------
    num_of_inputs : int, optional
        Inputs from either the source image or a previous layer

    activation_function : str
        Tells the node what activation type to use
        Supported activation types:
            -Sigmoid
            -ReLU

    Methods
    ------
    run(inputs=[0.12, 0.24])
        Executes the neurons function

    Examples
    --------
    >>> neuron1 = Neuron(4)
    >>> neuron2 = Neuron(10, 'sigmoid')
    >>> neuron3 = Neuron(2, 'relu')

    References
    ----------
        See : http://neuralnetworksanddeeplearning.com/chap1.html#sigmoid_neurons
              for the maths behind a Neuron

        See : https://cs231n.github.io/neural-networks-2/#init
            For network setup best practices
    """

    def __init__(self, num_of_inputs: int, activation_function='sigmoid'):
        self.weights = 0.1 * np.random.standard_normal(num_of_inputs)
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
        self.output = np.dot(inputs, self.weights)
        self.output += self.bias
        self.output = self.activation_function(self.output)
        return self.output


class Network:
    """
    A basic neural network

    Parameters
    ----------
    data_set : list
        EG: The MNIST dataset
    layers : dict
        Tells the network how to setup the layers
        In the form:
        layers = {
            'layer 1': {
                'activation': 'relu',
                'neurons': 10,
            },
            ...
        }

    Methods
    ------
    forward_prop
        forward propagation function

    back_prop
        back propagation function
    """

    def __init__(self, data_set: list, labels: list, layers: dict):
        self.layers = []
        self.labels = labels
        self.data_set = data_set
        self.learning_rate = 1

        for index, layer in enumerate(layers.values()):
            activation = layer['activation']
            num_of_neurons = layer['neurons']

            if index == 0:
                self.layers.append([Neuron(len(data_set[0]), activation) for num in range(num_of_neurons)])
            else:
                self.layers.append([Neuron(prev_num_of_neurons, activation) for num in range(num_of_neurons)])

            prev_num_of_neurons = num_of_neurons

    def forward_prop(self, data):
        """
        Passes input data through the network

        Parameters
        ----------
        data : list
            Your input data
        """
        layers = self.layers.copy()

        def feed_forward(input_arr):
            if len(layers) > 0:
                neuron_outputs = [neuron.run(input_arr) for neuron in layers[0]]
                del layers[0]
                feed_forward(neuron_outputs)

        feed_forward(data)

    def back_prop(self, labels: list, learning_rate=0.1):
        self.learning_rate = learning_rate
        output_layer = self.layers[-1]
        hidden_layers = self.layers[0:-1]
        hidden_layers.reverse()

        for label, output_neuron in zip(labels, output_layer):

            output_cost = 0.5 * (output_neuron.output - label) ** 2
            output_neuron.weights += output_cost * learning_rate

            for hidden_layer in hidden_layers:
                for hidden_neuron in hidden_layer:

                    hidden_cost = 0.5 * (hidden_neuron.output - label) ** 2
                    hidden_neuron.weights += hidden_cost * learning_rate

        hidden_layers.reverse()

    def train(self, epochs=1):
        for i in range(epochs):
            print(f"\nEpoch {i + 1}")
            for j in range(len(self.data_set)):
                print(f"\tData {j + 1}")
                self.forward_prop(self.data_set[j])
                self.back_prop(self.labels[j])


data_set = [[0.2, 0.41, 0.42, 0.11, 0.52]]

layers = {
    'layer 1': {
        'activation': 'sigmoid',
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

labels = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]


def output_to_file(name):
    with open(name, 'w') as network_file:
        np.set_printoptions(precision=4, linewidth=1000)
        for layer_index, layer in enumerate(network.layers):
            network_file.write(f'Layer {layer_index}:')
            for neuron_index, neuron in enumerate(layer):
                network_file.write(f'\n\tNeuron {neuron_index}:'
                                   f'\n\t\tWeights:'
                                   f'\n\t\t\t{neuron.weights}'
                                   f'\n\t\tOutput: {neuron.output}')
            network_file.write('\n')

        network_file.write('\nNetwork output:')


network = Network(data_set, labels, layers)
network.train(100)
for i in network.layers[-1]:
    print(f"Output: {i.output}")
output_to_file('network.txt')


