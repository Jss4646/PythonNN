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
        self.error_gradient = None

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
        output_no_activation = np.dot(inputs, self.weights) + self.bias
        self.output = self.activation_function(output_no_activation)
        return self.output


class Network:
    """
    A basic neural network

    Parameters
    ----------
    data_set : list
        EG: The MNIST dataset
    layers : dict- TODO remove the -
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
        self.layers: List[List[Neuron]] = []
        self.labels = labels
        self.data_set = data_set
        self.error = None
        self._initialise_layers(data_set, layers)

    def _initialise_layers(self, data_set, layers):
        prev_num_of_neurons = 0
        for index, layer in enumerate(layers.values()):
            activation = layer['activation']
            num_of_neurons = layer['neurons']
            layer_to_be_added = []

            if index == 0:
                self._add_input_layers(
                    activation,
                    data_set,
                    layer_to_be_added,
                    num_of_neurons
                )
            else:
                self._add_hidden_layers(
                    activation,
                    layer_to_be_added,
                    num_of_neurons,
                    prev_num_of_neurons
                )

            self.layers.append(layer_to_be_added)
            prev_num_of_neurons = num_of_neurons

    @staticmethod
    def _add_input_layers(activation, data_set, layer_to_be_added, num_of_neurons):
        for i in range(num_of_neurons):
            input_layer_size = len(data_set[0])
            neuron_to_be_added = Neuron(input_layer_size, activation)
            layer_to_be_added.append(neuron_to_be_added)

    @staticmethod
    def _add_hidden_layers(activation, layer_to_be_added, num_of_neurons, prev_num_of_neurons):
        for i in range(num_of_neurons):
            layer_size = prev_num_of_neurons
            neuron_to_be_added = Neuron(layer_size, activation)
            layer_to_be_added.append(neuron_to_be_added)

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
        """
        Generates the errors for each node

        Parameters
        ----------
        labels : list
            The input data for the network

        References
        ----------
            See : https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
                  Helped with backprop algorithm
        """
        self._gen_output_errors(labels)
        self._gen_hidden_errors()

    def _gen_output_errors(self, labels):
        """Generates errors for the output layer neuron and assigns them"""
        output_layer = self.layers[-1]
        output_layer_outputs = np.asarray([neuron.output for neuron in output_layer])
        labels = np.asarray(labels)

        output_errors = (labels - output_layer_outputs) * sigmoid(output_layer_outputs, True)
        for index, neuron in enumerate(output_layer):
            neuron.error_gradient = output_errors[index]

    def _gen_hidden_errors(self):
        """Uses the error calculated from the output layer to calculate the error for the previous layers"""
        self.layers.reverse()
        for index, layer in enumerate(self.layers[0:-1]):
            for neuron in self.layers[index + 1]:
                error = 0.0
                for output_neuron in layer:
                    error += sum(neuron.weights * output_neuron.error_gradient)
                neuron.error_gradient = error
        self.layers.reverse()

    def update_weights(self, data, learning_rate=0.1):
        """
        Uses the error from each neuron to calculate the amount to adjust the weight by

        Parameters
        ----------
        data : list
            The input data for the network

        learning_rate : float
            The learning rate for the network
            See Also: https://en.wikipedia.org/wiki/Learning_rate
        """
        self._update_input_weights(data, learning_rate)
        self._update_hidden_weights(learning_rate)

    def _update_input_weights(self, data, learning_rate):
        """Updates the input layer's weights"""
        input_layer = self.layers[0]
        for neuron in input_layer:
            for index, network_input in enumerate(data):
                neuron.weights[index] += learning_rate * neuron.error_gradient * network_input

    def _update_hidden_weights(self, learning_rate):
        """Updates the hidden layers weights"""
        hidden_layers = self.layers[1:]
        for index, layer in enumerate(hidden_layers):
            next_layer_outputs = [neuron.output for neuron in self.layers[index]]
            for neuron in layer:
                for neuron_index, next_layer_output in enumerate(next_layer_outputs):
                    neuron.weights[neuron_index] += learning_rate * neuron.error_gradient * next_layer_output

    def update_biases(self, learning_rate=0.1):
        """
        Updates all the biases in the network

        Parameters
        ----------
        learning_rate : float
            The learning rate for the network
            See Also: https://en.wikipedia.org/wiki/Learning_rate
        """
        for layer in self.layers:
            for neuron in layer:
                neuron.bias += learning_rate * neuron.error_gradient

    def calculate_error(self):
        outputs = np.array([neuron.output for neuron in self.layers[-1]])
        self.error = 0.5 * np.sum((self.labels - outputs) ** 2)
        return self.error

    def train(self, epochs: int = 1, learning_rate: float = 0.1):
        for epoch in range(epochs):

            if (epoch + 1) % 10 == 0 or epoch == 0:
                print(f"Epoch {epoch + 1}")

            for data, label in zip(self.data_set, self.labels):

                data_index = 0

                self.forward_prop(data)
                self.back_prop(label)
                self.update_weights(data, learning_rate)
                self.update_biases(learning_rate)

                if (epoch + 1) % 10 == 0 or epoch == 0:
                    print(f"\tData {data_index + 1}")
                    print(f"\t\tError {self.calculate_error()}\n")
                data_index += 1


data_set = [[0.2, 0.41, 0.42, 0.11, 0.52]]

layers = {
    'layer 1': {
        'activation': 'sigmoid',
        'neurons': 20,
    },
    'layer 2': {
        'activation': 'sigmoid',
        'neurons': 20,
    },
    'layer 3': {
        'activation': 'sigmoid',
        'neurons': 10,
    }
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

network.train(1000, 0.1)
for i in network.layers[-1]:
    print(f"Output: {i.output}")
print(f"\nError: {network.calculate_error()}")
