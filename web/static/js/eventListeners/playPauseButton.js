const playPauseButton = document.querySelector('.play-pause-button');

addHoverInteraction(playPauseButton);

playPauseButton.addEventListener('mouseup', function (event) {
    event.target.classList.replace('node-selected', 'node-hover');
});

playPauseButton.addEventListener('mousedown', function (event) {
    event.target.classList.replace('node-hover', 'node-selected');
});

playPauseButton.addEventListener('click', function () {

    const socket = io.connect(`${window.origin}`);

    network.apiNetwork.addLayers(1, 10);
    const networkJSON = network.apiNetwork.layers;

    socket.emit('start training', {
        data: networkJSON
    });

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
});