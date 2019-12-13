from flask import Flask, render_template, request
from Network import Network

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/setup-network', methods=['POST'])
def setup_network():
    layers = request.get_json()

    data_set = [[0.2, 0.41, 0.42, 0.11, 0.52]]
    labels = [[1, 1, 0, 0, 0, 0, 0, 0, 0, 0]]

    network = Network(data_set, labels, layers)
    network.train(1)
    return layers


if __name__ == '__main__':
    app.run()
