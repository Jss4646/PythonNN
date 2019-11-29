class viewportNetwork {
    constructor() {
        this.layers = document.querySelector('.layers');
    }

    /**
     * Creates a new layer and adds it to the layer group
     *
     * @param {int} numLayersAdded - number of layers to add, will add 1 if left blank
     * @param {int} numNodesInLayer - number of nodes to add to each layer, will add 1 if left blank
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
     * Adds a specified amount of nodes to a layer
     *
     * @param {object} layer - layer you want to add nodes too
     * @param {int} numNodesAdded - how many nodes you want to add, defaults to 1 if left blank
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
     *
     * @param {object} layer - layer that will be removed
     */
    removeLayer(layer) {
        const layers = this.layers.children;
        layer.remove();

        for (let i = 0; i < layers.length; i++) {
            layers[i].childNodes[0].innerText = `Layer ${i + 1}`;
        }
    };

    /**
     * Removes a node from a given layer
     *
     * @param {object} layer - layer that the node will be removed from
     */
    removeNode(layer) {
        const nodes = layer.querySelector('.layer-nodes');
        nodes.lastChild.remove();
    };
}