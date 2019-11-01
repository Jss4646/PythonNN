/**
 * @class
 * Remove or add layers to and from the network viewport
 *
 * @property {object} layers - Holds the html elements in the layers div
 *
 * @function {layer}  addLayer
 * @function {node}   addNode
 * @function          removeLayer
 * @function          removeNode
 *
 */
class Network {

    constructor() {
        this.layers = document.querySelector('.layers');
    }

    /**
     * Adds a layer to the network viewport
     * @returns {HTMLDivElement}
     */
    addLayer() {
        let numOfLayers = this.layers.childElementCount;

        const layer = document.createElement('div');
        layer.classList.add('layer');
        layer.id = `layer-${numOfLayers + 1}-viewport`;

        const title = document.createElement('h2');
        title.innerText = `Layer ${numOfLayers + 1}`;
        layer.appendChild(title);

        const nodes = document.createElement('div');
        nodes.classList.add('layer-nodes');
        layer.appendChild(nodes);

        this.layers.appendChild(layer);
        return layer;
    };

    /**
     * Adds a node to a given layer
     * @param layer
     * @returns {HTMLDivElement}
     */
    addNode(layer) {
        const nodeList = layer.querySelector('.layer-nodes');
        let numOfNodes = nodeList.childElementCount;

        const node = document.createElement('div');
        node.classList.add('node');
        node.classList.add('sigmoid-node');
        node.classList.add('no-hover');
        node.id = `l${layer.id.slice(6)}-node-${numOfNodes + 1}-viewport`;

        const nodeValue = document.createElement('span');
        nodeValue.innerText = '0.0';
        node.appendChild(nodeValue);

        nodeList.appendChild(node);
        return node
    };

    /**
     * Removes a given layer
     */
    removeLayer(layer) {
        layer.remove();
    };

    /**
     * Removes the last node from a layer
     * @param layer
     */
    removeNode(layer) {
        const nodes = layer.querySelector('.layer-nodes');
        nodes.childNodes[-1].remove();
    };
}

// const nn = new Network();
// nn.addLayers(4);
// nn.addNodes(nn.layers.childNodes[1],1);
