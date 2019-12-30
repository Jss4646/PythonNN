from typing import List, Any

import numpy as np
import random


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

    activation_function : str-
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

        See : https://cs231n.github.io/neural-netwworks-2/#init
            For network setup best practices
    """

    def __init__(self, num_of_inputs: int, activation_function='sigmoid'):
        self.weights = 0.1 * np.random.standard_normal(num_of_inputs)
        self.bias = 0.0
        self.output = 0.0
        self.output_no_activation = 0
        self.error = None

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
        self.output_no_activation = np.dot(inputs, self.weights) + self.bias
        self.output = self.activation_function(self.output_no_activation)
        return self.output


class Network:
    """
    A basic neural network

    Parameters
    ----------
    data_set : list
        EG: The MNIST dataset
    layers : dict-
        Tells the network how to setup the viewportLayers
        In the form:
        viewportLayers = {
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

        for index, layer in enumerate(layers.values()):
            activation = layer['activation']
            num_of_neurons = layer['neurons']

            if index == 0:
                self.layers.append([Neuron(len(data_set[0]), activation) for i in range(num_of_neurons)])
            else:
                self.layers.append([Neuron(prev_num_of_neurons, activation) for i in range(num_of_neurons)])

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

    def back_prop(self, labels: list):
        self._gen_output_errors(labels)
        self._gen_hidden_errors()

    def _gen_output_errors(self, labels):
        output_layer = self.layers[-1]
        output_layer_outputs = np.asarray([neuron.output for neuron in output_layer])
        labels = np.asarray(labels)

        output_errors = (labels - output_layer_outputs) * sigmoid(output_layer_outputs, True)
        for index, neuron in enumerate(output_layer):
            neuron.error = output_errors[index]

    def _gen_hidden_errors(self):
        self.layers.reverse()
        for index, layer in enumerate(self.layers[0:-1]):
            for neuron in self.layers[index + 1]:
                error = 0.0
                for output_neuron in layer:
                    error += sum(neuron.weights * output_neuron.error)
                neuron.error = error
        self.layers.reverse()

    def update_weights(self, data, learning_rate=0.1):
        self._update_input_weights(data, learning_rate)
        self._update_hidden_weights(learning_rate)

    def _update_input_weights(self, data, learning_rate):
        input_layer = self.layers[0]
        for neuron in input_layer:
            for index, network_input in enumerate(data):
                neuron.weights[index] += learning_rate * neuron.error * network_input

    def _update_hidden_weights(self, learning_rate):
        hidden_layers = self.layers[1:]
        for index, layer in enumerate(hidden_layers):

            next_layer_outputs = [neuron.output for neuron in self.layers[index + 1]]

            for neuron in layer:
                for weight, next_layer_output in zip(neuron.weights, next_layer_outputs):
                    weight += learning_rate * neuron.error * next_layer_output

    # def update_biases(self, learning_rate=0.1):
    #
    #     output_layer = self.layers[-1]
    #     hidden_layer = self.layers[0:-2]

    def train(self, epochs=1):
        for i in range(epochs):
            if (i + 1) % 10 == 0:
                print(f"\nEpoch {i + 1}")
            for j in range(len(self.data_set)):
                if (i + 1) % 10 == 0:
                    print(f"\tData {j + 1}")
                    print(f"\t\tError: {[i.error for i in self.layers[0]]}")
                self.forward_prop(self.data_set[j])
                self.back_prop(self.labels[j])
                self.update_weights(self.data_set[j], 1)


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

labels = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


def output_to_file(name, network):
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



