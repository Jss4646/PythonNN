const playPauseButton = document.querySelector('.play-pause-button');

playPauseButton.addEventListener('mouseenter', function (event) {
    event.target.classList.replace('no-hover', 'node-hover')
});

playPauseButton.addEventListener('mouseleave', function (event) {
    event.target.classList.replace('node-hover', 'no-hover')
});

playPauseButton.addEventListener('mouseup', function (event) {
    event.target.classList.replace('node-selected', 'node-hover');
});

playPauseButton.addEventListener('mousedown', function (event) {
    event.target.classList.replace('node-hover', 'node-selected');
});

playPauseButton.addEventListener('click', function (event) {

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