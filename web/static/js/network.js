/**
 * @class
 * The primary network that handles both the control and viewport GUI networks
 *
 * @property {controlNetwork}  controlNetwork - the control GUI network
 * @property {viewportNetwork} viewportNetwork - the viewport GUI network
 * @property (apiNetwork} apiNetwork - handles the layers json that will be sent off to the flask server
 *
 * @function  addLayers
 * @function  addNodes
 * @function  removeLayer
 * @function  removeNode
 *
 */
class Network {
    constructor() {
        this.controlNetwork = new controlNetwork();
        this.viewportNetwork = new viewportNetwork();
        this.apiNetwork = new apiNetwork();

        this.addLayers(4, 3);
    }

    /**
     * Adds a new layer to each GUI network
     *
     * @param {int} numLayersToAdd - number of layers to add, will add 1 if left blank
     * @param {int} numNodesInLayer - number of nodes to add to each layer, will add 1 if left blank
     */
    addLayers(numLayersToAdd = 1, numNodesInLayer = 1) {
        this.controlNetwork.addLayers(numLayersToAdd, numNodesInLayer);
        this.viewportNetwork.addLayers(numLayersToAdd, numNodesInLayer);
        this.apiNetwork.addLayers(numLayersToAdd, numNodesInLayer);
    }

    /**
     * Adds a specified amount of nodes to a layer
     *
     * @param {int} layerIndex - the index of the layer you want to add nodes too
     * @param {int} numNodesAdded - how many nodes you want to add, defaults to 1 if left blank
     */
    addNodes(layerIndex, numNodesAdded = 1) {
        this.controlNetwork.addNodes(layerIndex, numNodesAdded);
        this.viewportNetwork.addNodes(layerIndex, numNodesAdded);
        this.apiNetwork.addNodes(layerIndex, numNodesAdded);
    }

    /**
     * Removes a given layer
     *
     * @param {int} layerIndex - the index of the layer that will be removed
     */
    removeLayer(layerIndex) {
        if (this.controlNetwork.layers.childElementCount > 1) {
            this.controlNetwork.removeLayer(layerIndex);
            this.viewportNetwork.removeLayer(layerIndex);
            this.apiNetwork.removeLayer(layerIndex);
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
        if (this.controlNetwork.layers.querySelector('.node-list').childElementCount > 1) {
            this.controlNetwork.removeNode(layerIndex);
            this.viewportNetwork.removeNode(layerIndex);
            this.apiNetwork.removeNode(layerIndex);
        } else {
            console.log('The layer has to contain at least one node');
        }
    }

    wipeLayers() {
        this.controlNetwork.wipeLayers();
        this.viewportNetwork.wipeLayers();
        this.apiNetwork.wipeLayers();
    }
}

const network = new Network();
