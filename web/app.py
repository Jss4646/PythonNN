from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/setup-network', methods=['POST'])
def setup_network():
    layers = request.get_json()
    print(layers)
    pass


if __name__ == '__main__':
    app.run()
