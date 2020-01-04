import unittest
from Network import Neuron, sigmoid, relu, Network
import numpy as np

np.random.seed(0)


# TODO add more print statements
class NeuronTesting(unittest.TestCase):
    """

    """
    def setUp(self) -> None:
        self.labels = [[1, 0]]

        self.layers = {
            'layer 1': {
                'activation': 'sigmoid',
                'neurons': 2,
            },
            'layer 2': {
                'activation': 'sigmoid',
                'neurons': 2,
            }
        }

        self.data_set = [[0.2, 0.41, 0.42, 0.11, 0.52]]

        self.network = Network(self.data_set, self.labels, self.layers)

        self.neuron_inputs = [[0.23, 0.51, 0.24, 0.12], [], [1, -5, -200000, 2]]
        self.neuron_activations = ['sigmoid', 'sigmoid', 'relu']
        self.test_neurons = []

        for neuron_input, neuron_activation in zip(self.neuron_inputs, self.neuron_activations):
            self.add_neuron(neuron_input, neuron_activation)

    def add_neuron(self, neuron_input, neuron_activation):
        self.test_neurons.append(Neuron(len(neuron_input), neuron_activation))

    def test_sigmoid(self):
        print("\nSigmoid Test:")
        self.assertAlmostEqual(sigmoid(1), 0.731058, 5)
        self.assertAlmostEqual(sigmoid(1, True), 0.1966119, 5)

    def test_relu(self):
        print("\nRelu Test:")
        self.assertAlmostEqual(relu(1), 1)
        self.assertAlmostEqual(relu(0, True), 1)

    def test_neuron_init(self):
        print("\nNeuron init Test:")
        with self.assertRaises(ValueError):
            self.add_neuron([0], 'other')

    def test_weights(self):
        print("\nWeight init Test:")
        output_layer = self.network.layers[-1]
        for neuron in output_layer:
            print(f"\tNeuron Weights: {[np.around(i, 3) for i in neuron.weights]}")
            self.assertIsNotNone(neuron.weights)

    def test_neuron_run(self):
        print("\nRun Neuron Test:")
        for test_neuron, neuron_input in zip(self.test_neurons, self.neuron_inputs):
            test_neuron.run(neuron_input)
            print(f"Neuron output: {test_neuron.output}")
            print(f"Neuron type: {test_neuron.activation_function.__name__}")

            self.assertNotEqual(test_neuron.output, 0.0)

    def test_output_backprop(self):
        print("\nOutput Backprop Test:")
        output_layer = self.network.layers[-1]
        self.network._gen_output_errors([1, 0])
        self.assertEqual(output_layer[0].error_gradient, 1)

    def test_hidden_backprop(self):
        print("\nHidden Backprop Test:")
        hidden_layers = self.network.layers[0:-1]

        self.network._gen_output_errors(self.labels[0])
        self.network._gen_hidden_errors()

        hidden_errors = []
        for layer in hidden_layers:
            hidden_errors.append([neuron.error_gradient for neuron in layer])
        self.assertEqual(len(hidden_errors[0]), 2)

    def test_hidden_backprop_changes(self):
        print("\nHidden Backprop Changes Test:")
        self.network._gen_output_errors(self.labels[0])
        self.network._gen_hidden_errors()

        hidden_layers = self.network.layers[0:-1]
        previous_errors = []
        for layer in hidden_layers:
            previous_errors.append([neuron.error_gradient for neuron in layer])

        self.network.update_weights(self.data_set[0])
        self.network._gen_output_errors(self.labels[0])
        self.network._gen_hidden_errors()

        current_errors = []
        for layer in hidden_layers:
            current_errors.append([neuron.error_gradient for neuron in layer])

        self.assertNotEqual(current_errors, previous_errors)

    def test_update_input_weights(self):
        input_layer = self.network.layers[0]

        self.network._gen_output_errors([1, 0])
        self.network._gen_hidden_errors()

        previous_weights = []
        for neuron in input_layer:
            previous_weights.append([weight.copy() for weight in neuron.weights])

        self.network._update_input_weights(self.data_set[0], 0.1)

        current_weights = []
        for neuron in input_layer:
            current_weights.append([weight.copy() for weight in neuron.weights])
        self.assertNotEqual(previous_weights, current_weights)

    def test_update_hidden_weights(self):
        hidden_weights = self.network.layers[1:]

        self.network.forward_prop(self.data_set[0])
        self.network._gen_output_errors([1, 0])
        self.network._gen_hidden_errors()

        previous_weights = []
        for layer in hidden_weights:
            for neuron in layer:
                previous_weights.append([weight.copy() for weight in neuron.weights])

        self.network._update_hidden_weights(0.1)

        current_weights = []
        for layer in hidden_weights:
            for neuron in layer:
                current_weights.append([weight.copy() for weight in neuron.weights])

        print(f'First Sample: {previous_weights[0][0]}')
        print(f'Second Sample: {current_weights[0][0]}')
        self.assertNotEqual(previous_weights, current_weights)

    def test_get_layers(self):
        output_layers = self.network.get_layers()
        self.assertEqual(output_layers, self.layers)


# TODO add tests for network
if __name__ == '__main__':
    unittest.main()
