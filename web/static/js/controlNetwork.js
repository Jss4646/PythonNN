/**
 * @class
 * Controls the control network GUI
 *
 * @property {object} layers - holds the control network layers
 *
 * @function  addLayer
 * @function  addNode
 * @function  removeLayer
 * @function  removeNode
 *
 */
class controlNetwork {
    constructor() {
        this.layers = document.querySelector('.layer-list');
    }

    /**
     * Creates a new layer and adds it to the layer group
     *
     * @param {int} numLayersToAdd - number of layers to add, will add 1 if left blank
     * @param {int} numNodesInLayer - number of nodes to add to each layer, will add 1 if left blank
     */
    addLayer(numLayersToAdd = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersToAdd; i++) {
            const layerGroup = this.createLayer(numNodesInLayer);
            this.layers.appendChild(layerGroup);

            const layerIndex = this.layers.childNodes.length - 1;
            this.addNode(layerIndex, numNodesInLayer);
        }
    };

    /**
     * Adds a specified amount of nodes to a layer
     *
     * @param {int} layerIndex - the index of the layer you want to add nodes too
     * @param {int} numNodesAdded - how many nodes you want to add, defaults to 1 if left blank
     */
    addNode(layerIndex, numNodesAdded = 1) {

        const layer = document.querySelectorAll('.layer-group')[layerIndex];

        for (let i = 0; i < numNodesAdded; i++) {
            const nodeLayer = layer.querySelector('.node-list');
            let numOfNodes = nodeLayer.childElementCount;

            const node = this.createNode(numOfNodes);
            nodeLayer.appendChild(node);
        }
    };

    /**
     * Removes a given layer
     *
     * @param {int} layerIndex - the index of the layer that will be removed
     */
    removeLayer(layerIndex) {

        const layer = document.querySelectorAll('.layer-group')[layerIndex];

        const layers = this.layers.children;
        layer.remove();

        for (let i = 0; i < layers.length; i++) {
            layers[i].querySelector('.layer-text').innerText = `Layer ${i + 1}`
        }
    }

    /**
     * Removes a node from a given layer
     *
     * @param {int} layerIndex - the index of the layer that the node will be removed from
     */
    removeNode(layerIndex) {

        const layer = document.querySelectorAll('.layer-group')[layerIndex];

        const layerNodes = layer.querySelector('.node-list');
        layerNodes.lastChild.remove();
    }

    createLayer() {
        let numOfLayers = this.layers.childElementCount;

        const layerGroup = document.createElement('li');
        layerGroup.classList.add('layer-group');

        const layerBar = document.createElement('div');
        layerBar.classList.add('layer-bar');

        const deleteLayerIcon = document.createElement('img');
        deleteLayerIcon.classList.add('delete-layer');
        deleteLayerIcon.setAttribute('src', 'https://via.placeholder.com/20');
        addDeleteLayerInteraction(deleteLayerIcon);

        const layerText = document.createElement('span');
        layerText.classList.add('layer-text');
        layerText.innerText = `Layer ${numOfLayers + 1}`;

        const dropDownIcon = document.createElement('img');
        dropDownIcon.classList.add('drop-down-button');
        dropDownIcon.setAttribute('src', 'https://via.placeholder.com/20');
        addDropdownInteraction(dropDownIcon);

        layerBar.appendChild(deleteLayerIcon);
        layerBar.appendChild(layerText);
        layerBar.appendChild(dropDownIcon);

        layerGroup.appendChild(layerBar);

        const nodeList = document.createElement('ol');
        nodeList.classList.add('node-list');
        nodeList.classList.add('hidden-list');


        const nodeControls = document.createElement('div');
        nodeControls.classList.add('node-controls');
        nodeControls.classList.add('hidden-list');

        const removeNode = document.createElement('img');
        removeNode.classList.add('remove-node');
        removeNode.src = 'https://via.placeholder.com/20';
        addDeleteNodeInteraction(removeNode);

        const addNode = document.createElement('img');
        addNode.classList.add('add-node');
        addNode.src = 'https://via.placeholder.com/20';
        addAddNodeFunctionality(addNode);

        nodeControls.appendChild(removeNode);
        nodeControls.appendChild(addNode);

        layerGroup.appendChild(nodeList);
        layerGroup.appendChild(nodeControls);

        return layerGroup;
    }

    createNode(numOfNodes) {
        const node = document.createElement('li');
        node.innerText = `Node ${numOfNodes + 1}`;
        return node;
    }
}