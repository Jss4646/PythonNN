class viewportNetwork {
    constructor() {
        this.layers = document.querySelector('.layers');
    }

     /**
     * Adds a layer to the network viewport
     * @param numLayersAdded - optional, will add one layer and return it if left blank
     * @param numNodesInLayer - optional, will add one node to the layer if left blank
     */
    addLayer(numLayersAdded = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersAdded; i++) {
            let numOfLayers = this.layers.childElementCount;

            const layer = document.createElement('div');
            layer.classList.add('layer');

            const title = document.createElement('h2');
            title.innerText = `Layer ${numOfLayers + 1}`;
            layer.appendChild(title);

            const nodes = document.createElement('div');
            nodes.classList.add('layer-nodes');
            layer.appendChild(nodes);

            this.addNode(layer, numNodesInLayer);

            this.layers.appendChild(layer);
        }
    };

    /**
     * Adds a node to a given layer
     * @param layer - layer that node will be added to
     * @param numNodesAdded - optional, will add one node and return it if left blank
     */
    addNode(layer, numNodesAdded = 1) {
        for (let i = 0; i < numNodesAdded; i++) {
            const nodeList = layer.querySelector('.layer-nodes');

            const node = document.createElement('div');
            node.classList.add('node');
            node.classList.add('sigmoid-node');
            node.classList.add('no-hover');

            addNodeInteraction(node);

            const nodeValue = document.createElement('span');
            nodeValue.innerText = '0.0';
            node.appendChild(nodeValue);

            nodeList.appendChild(node);
        }
    };

    /**
     * Removes a given layer
     */
    removeLayer(layerIndex) {
        const layers = this.layers.children;

        layers[layerIndex].remove();

        //TODO update layer and node classes and titles
        for (let i = 0; i < layers.length; i++) {
            layers[i].childNodes[0].innerText = `Layer ${i + 1}`;
        }
    };

    /**
     * Removes the last node from a layer
     * @param layer - layer that node will be removed from
     */
    removeNode(layer) {
        const nodes = layer.querySelector('.layer-nodes');
        nodes.lastChild.remove();
    };
}