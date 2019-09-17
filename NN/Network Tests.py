import unittest
from Network import Neuron


def multiply(a, b):
    return a * b


class NeuronTesting(unittest.TestCase):
    def setUp(self) -> None:
        self.test_neurons = []

    def add_neuron(self, neuron_input, neuron_activation):
        self.test_neurons.append(Neuron(len(neuron_input), neuron_activation))

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


# TODO add tests for network
if __name__ == '__main__':
    unittest.main()
