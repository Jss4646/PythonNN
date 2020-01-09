const networkJSON = network.apiNetwork.layers;

fetch(`${window.origin}/setup-user`, {
    method: "POST",
   credentials: "include",
   body: JSON.stringify(networkJSON),
   cache: "no-cache",
   headers: new Headers({
       "content-type": "application/json"
   })
}).then(function (response) {
    response.text().then(function (strLayers) {
        if (strLayers !== 'Set user Cookie') {
            network.wipeLayers();
            let layers = JSON.parse(strLayers);
            for (let key in layers) {
                let numOfNeurons = layers[key].neurons;
                network.addLayers(1, numOfNeurons);
            }
            network.removeLayer(Object.keys(layers).length - 1);
        }
    })
});
