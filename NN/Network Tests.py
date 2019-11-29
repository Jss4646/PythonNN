import unittest
from Network import Neuron, sigmoid, relu, Network, labels, data_set, layers


# TODO add more print statements
class NeuronTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.test_neurons = []
        self.network = Network(data_set, labels, layers)

    def add_neuron(self, neuron_input, neuron_activation):
        self.test_neurons.append(Neuron(len(neuron_input), neuron_activation))

    def test_sigmoid(self):
        self.assertAlmostEqual(sigmoid(1), 0.731058, 5)
        self.assertAlmostEqual(sigmoid(1, True), 0.1966119, 5)

    def test_relu(self):
        self.assertAlmostEqual(relu(1), 1)
        self.assertAlmostEqual(relu(0, True), 1)

    def test_neuron_init(self):
        with self.assertRaises(ValueError):
            self.add_neuron([0], 'other')

        neuron_inputs = [[0.23, 0.51, 0.24, 0.12], [], [1, 5, 200000, -2]]
        neuron_activations = ['sigmoid', 'sigmoid', 'relu']

        for neuron_input, neuron_activation in zip(neuron_inputs, neuron_activations):
            self.add_neuron(neuron_input, neuron_activation)

    def test_neuron_run(self):
        for test_neuron in self.test_neurons:
            test_neuron.run()
            print(f"Neuron output: {test_neuron.output}")
            print(f"Neuron type: {type(test_neuron.output)}")
            self.assertNotEqual(test_neuron.output, 0)

    def test_network_backprop(self):
        before_backprop = self.network.layers[0][0].weights[0]
        self.network.back_prop(labels[0])
        after_backprop = self.network.layers[0][0].weights[0]
        self.assertNotEqual(before_backprop, after_backprop)


# TODO add tests for network
if __name__ == '__main__':
    unittest.main()
