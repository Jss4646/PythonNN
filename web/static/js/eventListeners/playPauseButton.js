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

    let frontend_outputs = document.querySelectorAll('.output-neurons li');
    let frontend_decision = document.querySelector('#decision');
    let frontend_label = document.querySelector('#actual');
    let frontend_epoch = document.querySelector('#epoch');

    socket.on('Network Outputs', function (data) {
        for (let i = 0; i < data.outputs.length; i++) {
            let decimalPoints = 10 ** 5;
            let output = Math.round(data.outputs[i] * decimalPoints) / decimalPoints;
            frontend_outputs[i].innerText = `${i}: ${output}`
        }
        frontend_decision.innerText = data.networkDecision;
        frontend_label.innerText = data.label;
        frontend_epoch.innerText = data.epoch;
    })
});