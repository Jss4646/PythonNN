const playPauseButton = document.querySelector('.play-pause-button');

addHoverInteraction(playPauseButton);

playPauseButton.addEventListener('mouseup', function (event) {
    event.target.classList.replace('node-selected', 'node-hover');
});

playPauseButton.addEventListener('mousedown', function (event) {
    event.target.classList.replace('node-hover', 'node-selected');
});

playPauseButton.addEventListener('click', function () {

    network.apiNetwork.addLayers(1, 10);
    const networkJSON = network.apiNetwork.layers;

    fetch(`${window.origin}/start-training`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(networkJSON),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    })
});