/**
 * @class
 * The primary network that handles both the control and viewport GUI networks
 *
 * @property {json} layers - the layers json
 *
 * @function  addLayers
 * @function  addNodes
 * @function  removeLayer
 * @function  removeNode
 *
 */
class apiNetwork {
    constructor() {
        this.layers = {}
    }

    /**
     * Adds a new layer to the layer json with given amount of nodes
     *
     * @param numLayersToAdd
     * @param numNodesInLayer
     */
    addLayers(numLayersToAdd = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersToAdd; i++) {
            const numOfLayers = Object.keys(this.layers).length;
            this.layers[`layer ${numOfLayers + 1}`] = {
                'activation': 'sigmoid',
                'neurons': numNodesInLayer,
            }
        }
    }

    /**
     * Increases the 'neurons' attribute by one in a given layer
     *
     * @param layerIndex
     * @param numNodesAdded
     */
    addNodes(layerIndex, numNodesAdded = 1) {
        const jsonLayerIndex = Object.keys(this.layers)[layerIndex];
        this.layers[jsonLayerIndex].neurons += numNodesAdded;
        console.log(this.layers);
    }

    /**
     * Removes a layer from the layers json
     *
     * @param layerIndex
     */
    removeLayer(layerIndex) {
        let jsonLayerIndex = Object.keys(this.layers)[layerIndex];
        delete this.layers[jsonLayerIndex];

        this.renameLayers();
        console.log(this.layers);
    }

    /**
     * Decreases the 'neurons' attribute by one in a given layer
     *
     * @param layerIndex
     */
    removeNode(layerIndex) {
        const jsonLayerIndex = Object.keys(this.layers)[layerIndex];
        this.layers[jsonLayerIndex].neurons -= 1;
    }

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
    renameLayers() {
        const layerKeys = Object.keys(this.layers);
        for (let i = 0; i < layerKeys.length; i++) {

            let jsonLayerIndex = layerKeys[i];

            if (jsonLayerIndex !== `layer ${i + 1}`) {
                this.layers[`layer ${i + 1}`] = this.layers[jsonLayerIndex];
                delete this.layers[jsonLayerIndex];
            }
        }
    }
}