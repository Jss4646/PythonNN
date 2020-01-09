import uuid
import numpy as np
from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
from Network import Network
from mlxtend.data import loadlocal_mnist

app = Flask(__name__)
app.config['SECRET_KEY'] = 'temp'
socketio = SocketIO(app)

inputs, raw_labels = loadlocal_mnist(
    images_path='NN/mnistDataset/train-images.idx3-ubyte',
    labels_path='NN/mnistDataset/train-labels.idx1-ubyte'
)

labels = np.zeros((len(raw_labels), 10))
for raw_label, label in zip(raw_labels, labels):
    label[raw_label - 1] = 1
labels = labels.tolist()

user_networks = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/setup-user', methods=['POST'])
def setup_user():
    user_cookie = request.cookies.get('PythonNNSession')
    if user_cookie and user_cookie in user_networks:
        user_network = user_networks[user_cookie]['network']
        network_layers = user_network.get_layers_json()
        return network_layers
    else:
        return set_cookie()


def set_cookie():
    user_id = str(uuid.uuid4())
    layers = request.get_json()
    user_networks[user_id] = {'network': Network(inputs[0:10], labels[0:10], layers)}
    res = make_response('Set user Cookie')
    res.set_cookie('PythonNNSession', user_id, max_age=60 * 60 * 24 * 365 * 2)
    return res


@socketio.on('start training')
def start_training(data):
    print('started')
    layers = data['data']
    user_id = request.cookies['PythonNNSession']

    network = Network(inputs[0:10], labels[0:10], layers)
    user_networks[user_id]['network'] = network

    epochs = 500
    learning_rate = 0.1

    train_network(epochs, learning_rate, network)


def train_network(epochs, learning_rate, network):
    for epoch in range(epochs):
        print(f"Epoch {epoch + 1}")
        for index, (data, label) in enumerate(zip(network.data_set, network.labels)):
            network.forward_prop(data)
            network.back_prop(label)
            network.update_weights(data, learning_rate)
            network.update_biases(learning_rate)

            if index % 1 == 0 or index == 0:
                network_outputs = [neuron.output for neuron in network.layers[-1]]

                print_network_details(index, label, network, network_outputs)

                # TODO make these available from the network
                network_details = {
                    'outputs': network_outputs,
                    'networkDecision': network_outputs.index(max(network_outputs)),
                    'label': label.index(max(label)),
                    'epoch': epoch + 1,
                }
                emit('Network Outputs', network_details)


def print_network_details(index, label, network, network_outputs):
    print(f"\tData {index}")
    print("\t\tOutputs:")

    for index, neuron in enumerate(network.layers[-1]):
        print(f"\t\t\t{index}: {neuron.output}")

    print(f'\t\tLabel: {label.index(max(label))}   '
          f'Guess: {network_outputs.index(max(network_outputs))}')
    print(f"\t\tError {network.calculate_error(label)}\n")


if __name__ == '__main__':
    socketio.run(app)
