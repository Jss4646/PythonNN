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

            switch (playPauseButton.state) {
                case "firstPlay":
                    playPauseButton._startNetwork(socket);
                    playPauseButton.switchState();
                    break;

                case 'pause':
                    playPauseButton._updateServerPauseState();
                    playPauseButton.switchState();
                    break;

                case 'play':
                    playPauseButton._updateServerPauseState();
                    playPauseButton._continueNetworkTraining(socket);
                    playPauseButton.switchState();
                    break;
            }
        })
    }

    _startNetwork(socket) {
        this._startNetworkTraining(socket);
        this._receiveNetworkData(socket);
    }

    _startNetworkTraining(socket) {
        const networkJSON = network.apiNetwork.layers;

        socket.emit('start training', {
            data: networkJSON
        });
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

    _continueNetworkTraining(socket) {
        socket.emit('continue training');
        this._receiveNetworkData(socket);
    }

    _updateServerPauseState() {
        fetch(`${window.origin}/set-pause-state`, {
            method: "POST",
            credentials: "include",
            body: this.state,
            cache: "no-cache",
        })
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