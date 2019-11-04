/**
 * @class
 * Remove or add layers to and from the network viewport
 *
 * @property {object}  layers - Holds the html elements in the layers div
 *
 * @function {layer}   addLayer
 * @function {node}    addNode
 * @function {boolean} removeLayer
 * @function {boolean} removeNode
 *
 */
class Network {

    constructor() {
        this.layers = document.querySelector('.layers');
    }

    /**
     * Adds a layer to the network viewport
     * @returns {HTMLDivElement}
     * @param numLayersAdded - optional, will add one layer and return it if left blank
     * @param numNodesInLayer - optional, will add one node to the layer if left blank
     */
    addLayer(numLayersAdded = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersAdded; i++) {
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

            this.addNode(layer, numNodesInLayer);

            this.layers.appendChild(layer);

            if (numLayersAdded === 1) {
                return layer;
            }
        }
    };

    /**
     * Adds a node to a given layer
     * @param layer - layer that node will be added to
     * @param numNodesAdded - optional, will add one node and return it if left blank
     * @returns {HTMLDivElement}
     */
    addNode(layer, numNodesAdded = 1) {
        for (let i = 0; i < numNodesAdded; i++) {
            const nodeList = layer.querySelector('.layer-nodes');
            let numOfNodes = nodeList.childElementCount;

            const node = document.createElement('div');
            node.classList.add('node');
            node.classList.add('sigmoid-node');
            node.classList.add('no-hover');
            node.id = `l${layer.id.slice(6)}-node-${numOfNodes + 1}-viewport`;

            addNodeInteraction(node);

            const nodeValue = document.createElement('span');
            nodeValue.innerText = '0.0';
            node.appendChild(nodeValue);

            nodeList.appendChild(node);
            if (numNodesAdded === 1) {
                return node;
            }
        }
    };

    /**
     * Removes a given layer
     * @returns {boolean} - True: Success, False: Failure
     */
    removeLayer(layer) {
        if (this.layers.children.length > 1) {
            layer.remove();
            return true;
        } else {
            console.log('The network has to contain at least one layer');
            return false;
        }
    };

    /**
     * Removes the last node from a layer
     * @param layer - layer that node will be removed from
     * @returns {boolean} - True: Success, False: Failure
     */
    removeNode(layer) {
        const nodes = layer.querySelector('.layer-nodes');

        if (nodes.childNodes.length > 1) {
            nodes.childNodes[0].remove();
            return true;
        } else {
            console.log('The layer has to contain at least one node');
            return false;
        }
    };
}

const nn = new Network();
nn.addLayer(4, 4);

