import numpy as np
from flask import Flask, render_template, request
from Network import Network
from mlxtend.data import loadlocal_mnist

app = Flask(__name__)

data_set, raw_labels = loadlocal_mnist(
    images_path='NN/mnistDataset/train-images.idx3-ubyte',
    labels_path='NN/mnistDataset/train-labels.idx1-ubyte'
)

labels = np.zeros((len(raw_labels), 10))
for raw_label, label in zip(raw_labels, labels):
    label[raw_label - 1] = 1


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/start-training', methods=['POST'])
def start_training():
    layers = request.get_json()

    network = Network(data_set[0:200], labels.tolist()[0:200], layers)

    return layers


if __name__ == '__main__':
    app.run()
