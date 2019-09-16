import unittest
from Network import Neuron


def multiply(a, b):
    return a * b


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.neuron_input = [0.02, 0.21, 0.01, 0.24]
        self.test_neuron = Neuron(self.neuron_input)

    def test_neuron_init(self):
        self.assertEqual(len(self.test_neuron.weights), len(self.neuron_input),
                         "It created the wrong amount of weights")

    def test_neuron_run(self):
        self.test_neuron.run()
        print(f"Neuron output: {self.test_neuron.output}")
        print(f"Neuron type: {type(self.test_neuron.output)}")
        self.assertNotEqual(self.test_neuron.output, 0)


if __name__ == '__main__':
    unittest.main()
