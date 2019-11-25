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
        this.viewportLayers = document.querySelector('.layers');
        this.controlLayers = document.querySelector('.layer-list');
    }

    /**
     * Adds a layer to the network viewport
     * @returns {HTMLDivElement}
     * @param numLayersAdded - optional, will add one layer and return it if left blank
     * @param numNodesInLayer - optional, will add one node to the layer if left blank
     */
    addViewportLayer(numLayersAdded = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersAdded; i++) {
            let numOfLayers = this.viewportLayers.childElementCount;

            const layer = document.createElement('div');
            layer.classList.add('layer');
            layer.id = `layer-${numOfLayers + 1}-viewport`;

            const title = document.createElement('h2');
            title.innerText = `Layer ${numOfLayers + 1}`;
            layer.appendChild(title);

            const nodes = document.createElement('div');
            nodes.classList.add('layer-nodes');
            layer.appendChild(nodes);

            this.addViewportNode(layer, numNodesInLayer);

            this.viewportLayers.appendChild(layer);

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
    addViewportNode(layer, numNodesAdded = 1) {
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
    removeViewportLayer(layer) {
        if (this.viewportLayers.children.length > 1) {
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
    removeViewportNode(layer) {
        const nodes = layer.querySelector('.layer-nodes');

        if (nodes.childNodes.length > 1) {
            nodes.childNodes[0].remove();
            return true;
        } else {
            console.log('The layer has to contain at least one node');
            return false;
        }
    };

    addControlLayer(numLayersAdded = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersAdded; i++) {
            let numOfLayers = this.controlLayers.childElementCount;

            const layerGroup = document.createElement('li');
            layerGroup.classList.add('layer-group');
            layerGroup.id = `layer-${numOfLayers + 1}`;

            const layerBar = document.createElement('div');
            layerBar.classList.add('layer-bar');

            const deleteLayerIcon = document.createElement('img');
            deleteLayerIcon.classList.add('delete-layer');
            deleteLayerIcon.scr = 'https://via.placeholder.com/20';
            //TODO add functionality to delete layer

            const layerText = document.createElement('span');
            layerText.classList.add('layer-text');
            layerText.innerText = `Layer ${numOfLayers + 1}`;

            const dropDownIcon = document.createElement('img');
            dropDownIcon.classList.add('drop-down-button');
            dropDownIcon.src = 'https://via.placeholder.com/20';
            //TODO add functionality to drop down

            layerBar.appendChild(deleteLayerIcon);
            layerBar.appendChild(layerText);
            layerBar.appendChild(dropDownIcon);

            layerGroup.appendChild(layerBar);

            const nodeList = document.createElement('ol');
            nodeList.classList.add('node-list');
            //TODO make nodes inside node div
            layerGroup.appendChild(nodeList);

            this.addControlNode(layerGroup, numNodesInLayer);

            this.controlLayers.appendChild(layerGroup);

            if (numLayersAdded === 1) {
                return layerGroup;
            }
        }
    };

    addControlNode(layer, numNodesAdded = 1) {
        let numOfLayers = this.controlLayers.childElementCount;

        for (let i = 0; i < numNodesAdded; i++) {
            const nodeLayer = layer.querySelector('.node-list');
            let numOfNodes = nodeLayer.childElementCount;

            const node = document.createElement('li');
            node.id = `l${numOfLayers + 1}-node-${numOfNodes + 1}`;
            node.innerText = `Node ${numOfNodes + 1}`;

            nodeLayer.appendChild(node);

            if (numNodesAdded === 1) {
                return node;
            }
        }

    };
}

const nn = new Network();
nn.addViewportLayer(4, 4);

