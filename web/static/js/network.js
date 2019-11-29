/**
 * @class
 * The primary network that handles both the control and viewport GUI networks
 *
 * @property {controlNetwork}  controlNetwork - the control GUI network
 * @property {viewportNetwork} viewportNetwork - the viewport GUI network
 *
 * @function  addLayer
 * @function  addNode
 * @function  removeLayer
 * @function  removeNode
 *
 */
class Network {
    constructor() {
        this.controlNetwork = new controlNetwork();
        this.viewportNetwork = new viewportNetwork();
    }

    /**
     * Adds a new layer to each GUI network
     *
     * @param {int} numLayersAdded - number of layers to add, will add 1 if left blank
     * @param {int} numNodesInLayer - number of nodes to add to each layer, will add 1 if left blank
     */
    addLayer(numLayersAdded = 1, numNodesInLayer = 1) {
        this.controlNetwork.addLayer(numLayersAdded, numNodesInLayer);
        this.viewportNetwork.addLayer(numLayersAdded, numNodesInLayer);
    }

    /**
     * Adds a specified amount of nodes to a layer
     *
     * @param {int} layerIndex - the index of the layer you want to add nodes too
     * @param {int} numNodesAdded - how many nodes you want to add, defaults to 1 if left blank
     */
    addNode(layerIndex, numNodesAdded = 1) {
        const controlLayer = document.querySelectorAll('.layer-group')[layerIndex];
        this.controlNetwork.addNode(controlLayer, numNodesAdded);

        const viewportLayer = document.querySelectorAll('.layer')[layerIndex];
        this.viewportNetwork.addNode(viewportLayer, numNodesAdded);
    }

    /**
     * Removes a given layer
     *
     * @param {int} layerIndex - the index of the layer that will be removed
     */
    removeLayer(layerIndex) {
        const controlLayer = document.querySelectorAll('.layer-group')[layerIndex];
        const viewportLayer = document.querySelectorAll('.layer')[layerIndex];

        if (this.controlNetwork.layers.childElementCount > 1) {
            this.controlNetwork.removeLayer(controlLayer);
            this.viewportNetwork.removeLayer(viewportLayer);
        } else {
            console.log('The network has to contain at least one layer');
        }
    }

    /**
     * Removes a node from a given layer
     *
     * @param {int} layerIndex - index of the layer that the node will be removed from
     */
    removeNode(layerIndex) {
        const controlLayer = document.querySelectorAll('.layer-group')[layerIndex];
        const viewportLayer = document.querySelectorAll('.layer')[layerIndex];

        if (controlLayer.querySelector('.node-list').childElementCount > 1) {
            this.controlNetwork.removeNode(controlLayer);
            this.viewportNetwork.removeNode(viewportLayer);
        } else {
            console.log('The layer has to contain at least one node');
        }
    }
}

const nn = new Network();
nn.addLayer(3, 3);

