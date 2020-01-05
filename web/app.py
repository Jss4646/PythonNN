import uuid
import numpy as np
from flask import Flask, render_template, request, make_response
from Network import Network
from mlxtend.data import loadlocal_mnist

app = Flask(__name__)


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


@app.route('/set-cookie', methods=['POST'])
def set_cookie():
    # TODO handel cookies that were before reset
    user_cookie = request.cookies.get('PythonNNSession')
    if user_cookie:
        user_network = user_networks[user_cookie]['network']
        network_layers = user_network.get_layers_json()
        return network_layers
    else:
        user_id = str(uuid.uuid4())

        layers = request.get_json()
        user_networks[user_id] = {'network': Network(inputs[0:200], labels[0:200], layers)}

        res = make_response('Set user Cookie')
        res.set_cookie('PythonNNSession', user_id, max_age=60 * 60 * 24 * 365 * 2)
        return res


@app.route('/start-training', methods=['POST'])
def start_training():
    layers = request.get_json()
    user_id = request.cookies['PythonNNSession']

    new_user_network = Network(inputs[0:200], labels[0:200], layers)
    user_networks[user_id]['network'] = new_user_network

    new_user_network.train()
    return 'Done Training!'


if __name__ == '__main__':
    app.run()
