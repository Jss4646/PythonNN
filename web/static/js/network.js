/**
 * @class
 * Remove or add layers to and from the network viewport
 *
 * @property {object}  layers - Holds the html elements in the layers div
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

    addLayer(numLayersAdded = 1, numNodesInLayer = 1) {
        this.controlNetwork.addLayer(numLayersAdded, numNodesInLayer);
        this.viewportNetwork.addLayer(numLayersAdded, numNodesInLayer);
    }

    addNode(layerIndex, numNodesAdded = 1) {
        const controlLayer = document.querySelectorAll('.layer-group')[layerIndex];
        this.controlNetwork.addNode(controlLayer, numNodesAdded);

        const viewportLayer = document.querySelectorAll('.layer')[layerIndex];
        this.viewportNetwork.addNode(viewportLayer, numNodesAdded);
    }

    removeLayer(layerIndex) {
        if (this.controlNetwork.layers.childElementCount > 1) {
            this.viewportNetwork.removeLayer(layerIndex);
            this.controlNetwork.removeLayer(layerIndex);
        } else {
            console.log('The network has to contain at least one layer');
        }
    }

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

