from typing import List

import numpy as np
from mlxtend.data import loadlocal_mnist


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
    def __init__(self, num_of_inputs: int, activation_function='sigmoid'):
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
        passes the inputs through the network

    back_prop
        generates the errors for each neuron

    update_weights
        updates the weights for each neuron

    calculate_error
        calculates the error for the output layer

    train
        trains the network
    """

    def __init__(self, input_array_length: int, layers: dict):
        self.layers: List[List[Neuron]] = []
        self.error = None

        self.num_of_epochs = 1
        self.learning_rate = 0.1

        self._initialise_layers(input_array_length, layers)

    def _initialise_layers(self, input_array_length, layers):
        prev_num_of_neurons = 0
        for index, layer in enumerate(layers.values()):
            activation = layer['activation']
            num_of_neurons = layer['neurons']

            if index == 0:
                layer_to_be_added = self._construct_layer(activation, input_array_length, num_of_neurons)
            else:
                layer_to_be_added = self._construct_layer(activation, prev_num_of_neurons, num_of_neurons)

            self.layers.append(layer_to_be_added)
            prev_num_of_neurons = num_of_neurons

    @staticmethod
    def _construct_layer(activation, prev_layer_size, num_of_neurons):

        layer_to_be_added = []

        for i in range(num_of_neurons):
            neuron_to_be_added = Neuron(prev_layer_size, activation)
            layer_to_be_added.append(neuron_to_be_added)

        return layer_to_be_added

    def update_layers(self, input_array_length: int, new_layers: dict):
        self.layers = []
        self._initialise_layers(input_array_length, new_layers)

    def get_layers_json(self):
        layers_json = {}
        for index, layer in enumerate(self.layers):
            activation = layer[0].activation_function.__name__
            num_of_neurons = len(layer)
            layers_json[f'layer{index + 1}'] = {'activation': activation, 'neurons': num_of_neurons}
        return layers_json

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

        output_errors = (labels - output_layer_outputs)
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

    def update_weights(self, data):
        """
        Uses the error from each neuron to calculate the amount to adjust the weight by

        Parameters
        ----------
        data : list-
            The input data for the network
        """
        self._update_input_weights(data)
        self._update_hidden_weights()

    def _update_input_weights(self, data: list):
        """Updates the input layer's weights"""
        input_layer = self.layers[0]
        for neuron in input_layer:
            for index, network_input in enumerate(data):
                neuron.weights[index] += self.learning_rate * neuron.error_gradient * network_input

    def _update_hidden_weights(self):
        """Updates the hidden layers weights"""
        hidden_layers = self.layers[1:]
        for index, layer in enumerate(hidden_layers):
            next_layer_outputs = [neuron.output for neuron in self.layers[index]]
            for neuron in layer:
                for neuron_index, next_layer_output in enumerate(next_layer_outputs):
                    neuron.weights[neuron_index] += self.learning_rate * neuron.error_gradient * next_layer_output

    def update_biases(self):
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
                neuron.bias += self.learning_rate * neuron.error_gradient

    def add_layer(self, num_of_neurons, activation_type='sigmoid'):
        previous_layer_size = len(self.layers[-1])
        new_layer = self._construct_layer(activation_type, previous_layer_size, num_of_neurons)
        self.layers.append(new_layer)

    def remove_layer(self, index):
        del self.layers[index]

    def calculate_error(self, labels):
        """
        Calculate the sum error for the output layer

        Parameters
        ----------
        labels : list
            What the output of the network should be

        Returns
        -------
        error : float
            The error of the output layer
        """
        outputs = np.array([neuron.output for neuron in self.layers[-1]])
        self.error = 0.5 * np.sum((labels - outputs) ** 2)
        return self.error

    def get_outputs(self):
        outputs = [neuron.output for neuron in self.layers[-1]]
        return outputs

    def train(self):
        for epoch in range(self.num_of_epochs):
            print(f"Epoch {epoch + 1}")
            data_index = 0
            for data, label in zip(self.data_set, self.labels):
                self.forward_prop(data)
                self.back_prop(label)
                self.update_weights(data)
                self.update_biases()

                if (data_index + 1) % 10 == 0 or data_index == 0:
                    print(f"\tData {data_index + 1}")

                    print("\t\tOutputs:")
                    for index, neuron in enumerate(self.layers[-1]):
                        print(f"\t\t\t{index}: {neuron.output}")

                    network_outputs = [neuron.output for neuron in self.layers[-1]]
                    print(f'\t\tLabel: {label.index(max(label))}   '
                          f'Guess: {network_outputs.index(max(network_outputs))}')

                    print(f"\t\tError {self.calculate_error(label)}\n")
                data_index += 1

#
# data_set, raw_labels = loadlocal_mnist(
#     images_path='mnistDataset/train-images.idx3-ubyte',
#     labels_path='mnistDataset/train-labels.idx1-ubyte'
# )
#
# labels = np.zeros((len(raw_labels), 10))
# for raw_label, label in zip(raw_labels, labels):
#     label[raw_label - 1] = 1

layers = {
    'layer 1': {
        'activation': 'sigmoid',
        'neurons': 10,
    },
    'layer 2': {
        'activation': 'sigmoid',
        'neurons': 20,
    },
    'layer 3': {
        'activation': 'sigmoid',
        'neurons': 10,
    },
}
# np.random.seed(0)
# network = Network(data_set[0:200], labels[0:200], layers)
# network.train(1, 0.01)


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
