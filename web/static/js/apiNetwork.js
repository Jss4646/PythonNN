class apiNetwork {
    constructor() {
        this.layers = {}
    }

    addLayers(numLayersToAdd = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersToAdd; i++) {
            const numOfLayers = Object.keys(this.layers).length;
            this.layers[`layer-${numOfLayers + 1}`] = {
                'activation': 'sigmoid',
                'neurons': numNodesInLayer,
            }
        }
    }

    addNodes(layerIndex, numNodesAdded = 1) {

    }

    removeLayer(layerIndex) {
        const jsonLayerIndex = Object.keys(this.layers)[layerIndex];
        delete this.layers[jsonLayerIndex];
    }

    removeNode(layerIndex) {

    }
}