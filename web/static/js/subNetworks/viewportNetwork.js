/**
 * @class
 * Controls the control network Control GUI
 *
 * @property {object} layers - holds the control network layers
 *
 * @function  addLayers
 * @function  addNodes
 * @function  removeLayer
 * @function  removeNode
 *
 */
class viewportNetwork {
    constructor() {
        this.layers = document.querySelector('.layers');
    }

    /**
     * Creates a new layer and adds it to the layer group
     *
     * @param {int} numLayersToAdd - number of layers to add, will add 1 if left blank
     * @param {int} numNodesInLayer - number of nodes to add to each layer, will add 1 if left blank
     */
    addLayers(numLayersToAdd = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersToAdd; i++) {
            const layer = this.createLayer();

            const layerIndex = this.layers.childNodes.length;
            this.layers.appendChild(layer);

            this.addNodes(layerIndex, numNodesInLayer);
        }
    };

    /**
     * Adds a specified amount of nodes to a layer
     *
     * @param {int} layerIndex - the index of the layer you want to add nodes too
     * @param {int} numNodesAdded - how many nodes you want to add, defaults to 1 if left blank
     */
    addNodes(layerIndex, numNodesAdded = 1) {

        const layer = document.querySelectorAll('.layer')[layerIndex];

        for (let i = 0; i < numNodesAdded; i++) {
            const nodeList = layer.querySelector('.layer-nodes');
            const node = this.createNode();
            nodeList.appendChild(node);
        }
    };

    /**
     * Removes a given layer
     *
     * @param {int} layerIndex - layer that will be removed
     */
    removeLayer(layerIndex) {

        const layer = document.querySelectorAll('.layer')[layerIndex];

        const layers = this.layers.children;
        layer.remove();

        this.renameLayers(layers);
    };

    /**
     * Removes a node from a given layer
     *
     * @param {int} layerIndex - the index of the layer that the node will be removed from
     */
    removeNode(layerIndex) {

        const layer = document.querySelectorAll('.layer')[layerIndex];

        const nodes = layer.querySelector('.layer-nodes');
        nodes.lastChild.remove();
    };

    /**
     * Renames all the layers in the network so they are in order
     * EG:
     * layer 1
     * layer 2
     * layer 4
     *
     * Becomes
     *
     * layer 1
     * layer 3
     * layer 2
     */
    renameLayers(layers) {
        for (let i = 0; i < layers.length; i++) {
            layers[i].childNodes[0].innerText = `Layer ${i + 1}`;
        }
    }

    /**
     * Creates a layer for the network
     *
     * @returns {HTMLDivElement}
     */
    createLayer() {
        let numOfLayers = this.layers.childElementCount;

        const layer = document.createElement('div');
        layer.classList.add('layer');

        const title = document.createElement('h2');
        title.innerText = `Layer ${numOfLayers + 1}`;
        layer.appendChild(title);

        const nodes = document.createElement('div');
        nodes.classList.add('layer-nodes');
        layer.appendChild(nodes);
        return layer;
    }

    /**
     * Creates a node for a network layer
     *
     * @returns {HTMLDivElement}
     */
    createNode() {
        const node = document.createElement('div');
        node.classList.add('node');
        node.classList.add('sigmoid-node');
        node.classList.add('no-hover');

        addNodeInteraction(node);

        const nodeValue = document.createElement('span');
        nodeValue.innerText = '0.0';
        node.appendChild(nodeValue);
        return node;
    }
}