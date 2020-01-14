class PlayPauseButton {
    constructor() {
        this.htmlElement = document.querySelector('.play-pause-button');
        this.state = 'firstPlay';
        const playPauseButton = this;

        this._addEventListeners();
    }

    _addEventListeners() {
        addHoverInteraction(this.htmlElement);

        this.htmlElement.addEventListener('mouseup', function (event) {
            event.target.classList.replace('node-selected', 'node-hover');
        });

        this.htmlElement.addEventListener('mousedown', function (event) {
            event.target.classList.replace('node-hover', 'node-selected');
        });

        this.htmlElement.addEventListener('click', function () {

            const socket = io.connect(`${window.origin}`);

            switch (playPauseButton.state) {
                case 'firstPlay':

                    playPauseButton._startNetwork(socket);
                    playPauseButton.switchState();
                    break;

                case 'pause':

                    playPauseButton.switchState();
                    break;

                case 'play':

                    playPauseButton.switchState();
                    break;
            }
        })
    }

    _startNetwork(socket) {
        this._sendNetworkData(socket);
        this._receiveNetworkData(socket);
    }

    _receiveNetworkData(socket) {
        let frontendOutputs = document.querySelectorAll('.output-neurons li');
        let frontendDecision = document.querySelector('#decision');
        let frontendLabel = document.querySelector('#actual');
        let frontendEpoch = document.querySelector('#epoch');

        socket.on('Network Outputs', function (data) {
            for (let i = 0; i < data.outputs.length; i++) {
                let decimalPoints = 10 ** 5;
                let output = Math.round(data.outputs[i] * decimalPoints) / decimalPoints;
                frontendOutputs[i].innerText = `${i}: ${output}`
            }
            frontendDecision.innerText = data.networkDecision;
            frontendLabel.innerText = data.label;
            frontendEpoch.innerText = data.epoch;
        })
    }

    _sendNetworkData(socket) {
        network.apiNetwork.addLayers(1, 10);
        const networkJSON = network.apiNetwork.layers;

        socket.emit('start training', {
            data: networkJSON
        });
    }

    switchState() {
        switch (this.state) {
            case 'firstPlay':
                this.state = 'pause';
                break;

            case 'play':
                this.state = 'pause';
                break;

            case 'pause':
                this.state = 'play';
                break;
        }
    }
}

const playPauseButton = new PlayPauseButton();