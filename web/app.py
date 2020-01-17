import uuid
import numpy as np
from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO, emit
from Network import Network
from mlxtend.data import loadlocal_mnist
import ast

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

users = {}


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/setup-user', methods=['POST'])
def setup_user():
    user_cookie = request.cookies.get('PythonNNSession')
    if user_cookie and user_cookie in users:
        user_network = users[user_cookie]['network']
        network_layers = user_network.get_layers_json()
        return network_layers
    else:
        return add_user()


def add_user():
    user_id = str(uuid.uuid4())
    add_user_to_users(user_id)

    cookie_data = {'userId': user_id, 'pauseState': 'firstPlay'}
    return create_user_cookie(cookie_data)


def add_user_to_users(user_id):
    layers = request.get_json()
    users[user_id] = {
        'network': Network(len(inputs[0]), layers),
        'dataSet': Rememberable(inputs, labels),
        'epoch': 0,
    }


def create_user_cookie(cookie_data):
    response = make_response('Set user Cookie')
    response.set_cookie('PythonNNSession', str(cookie_data), max_age=60 * 60 * 24 * 365 * 2)
    return response


@app.route('/set-pause-state', methods=['POST'])
def set_pause_state():
    user_cookie = ast.literal_eval(request.cookies.get('PythonNNSession'))
    new_state = request.data

    user_id = user_cookie['userId']
    cookie_data = {'userId': user_id, 'pauseState': new_state}
    updated_cookie = create_user_cookie(cookie_data)

    return updated_cookie


@socketio.on('start training')
def start_training(data):
    print('started')
    layers = data['data']
    user_cookie = ast.literal_eval(request.cookies['PythonNNSession'])
    user_id = user_cookie['userId']
    print(f'User ID: {user_id}')
    print(f'Layers: {layers}')

    user = users[user_id]
    network = users[user_id]['network']

    network.num_of_epochs = 50
    network.learning_rate = 0.1

    network.add_layer(10)
    train_network(user)
    network.remove_layer(-1)


def train_network(user):
    network = user['network']
    for epoch in range(network.num_of_epochs):
        print(f"Epoch {epoch + 1}")
        for index, (data, label) in user['dataSet']:

            propagate_network(data, label, network)

            if index % 10 == 0 or index == 0:
                network_outputs = network.get_outputs()

                # print_network_details(index, label, network, network_outputs)
                send_network_data(epoch, label, network_outputs)

            user_cookie = ast.literal_eval(request.cookies.get('PythonNNSession'))
            pause_state = user_cookie['pauseState']
            if pause_state == 'pause':
                break


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


if __name__ == '__main__':
    socketio.run(app)


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
