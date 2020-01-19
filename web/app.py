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

inputs = inputs[0:10]
labels = labels[0:10]


class Rememberable:
    def __init__(self, source1, source2):
        self.index = 0
        self.source1, self.source2 = source1, source2
        self.source = zip(source1, source2)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index != len(self.source1):
            item1 = self.source1[self.index]
            item2 = self.source2[self.index]

            output = (self.index, (item1, item2))
            self.index += 1
            return output
        else:
            self.index = 0
            raise StopIteration


class User:
    def __init__(self, inputs, layers):
        self.network = Network(len(inputs[0]), layers)
        self.data_set = Rememberable(inputs, labels)
        self.epoch = None
        self.play_pause_state = 'firstPlay'
        self.layer_index = None
        self.node_index = None

    def switch_play_pause_state(self, new_state):
        self.play_pause_state = new_state


users = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/setup-user', methods=['POST'])
def setup_user():
    user_id = request.cookies.get('PythonNNSession')
    if user_id and user_id in users:
        user_network = users[user_id].network
        network_layers = user_network.get_layers_json()
        return network_layers
    else:
        return add_user()


def add_user():
    user_id = str(uuid.uuid4())
    add_user_to_users(user_id)

    return create_user_cookie(user_id)


def add_user_to_users(user_id):
    layers = request.get_json()
    users[user_id] = User(inputs, layers)


def create_user_cookie(cookie_data):
    response = make_response('Set user Cookie')
    response.set_cookie('PythonNNSession', str(cookie_data), max_age=60 * 60 * 24 * 365 * 2)
    return response


@app.route('/set-pause-state', methods=['POST'])
def set_pause_state():
    user_id = request.cookies.get('PythonNNSession')
    new_state = request.data.decode('utf-8')
    user = users[user_id]
    user.switch_play_pause_state(new_state)
    return new_state


@socketio.on('start training')
def start_training(data):
    print('started')
    layers = data['data']
    user_id = request.cookies.get('PythonNNSession')
    print(f'User ID: {user_id}')
    print(f'Layers: {layers}')

    user = users[user_id]
    network = user.network

    user.epoch = 50
    network.learning_rate = 0.1

    network.add_layer(10)
    train_network(user)
    network.remove_layer(-1)


@socketio.on('continue training')
def continue_training():
    user_id = request.cookies.get('PythonNNSession')
    user = users[user_id]
    network = user.network

    network.add_layer(10)
    train_network(user)
    network.remove_layer(-1)


def train_network(user):
    network = user.network
    for epoch in range(user.epoch):
        print(f"Epoch {user.epoch - epoch}")
        for index, (data, label) in user.data_set:

            propagate_network(data, label, network)

            if index % 10 == 0 or index == 0:
                network_outputs = network.get_outputs()

                # print_network_details(index, label, network, network_outputs)
                send_network_data(user.epoch - epoch - 2, label, network_outputs)
                send_node_data(network, user)

            pause_state = user.play_pause_state
            if pause_state == 'pause':
                user.epoch -= epoch
                return


def propagate_network(data, label, network):
    network.forward_prop(data)
    network.back_prop(label)
    network.update_weights(data)
    network.update_biases()


def send_network_data(epoch, label, network_outputs):
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


@socketio.on('send node data')
def receive_node_data(data):
    user_id = request.cookies.get('PythonNNSession')
    user = users[user_id]
    network = user.network

    user.layer_index, user.node_index = data['layerIndex'], data['nodeIndex']
    send_node_data(network, user)


def send_node_data(network, user):
    if user.layer_index:
        neuron = network.layers[user.layer_index][user.node_index]
        neuron_data = {
            'weights': neuron.weights.tolist(),
            'bias': neuron.bias,
            'output': neuron.output,
            'activationType': neuron.activation_function.__name__,
        }
        emit('neuron data', neuron_data)


if __name__ == '__main__':
    socketio.run(app, port=5001)
