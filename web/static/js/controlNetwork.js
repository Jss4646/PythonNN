class controlNetwork {
    constructor() {
        this.layers = document.querySelector('.layer-list');
    }

    addLayer(numLayersAdded = 1, numNodesInLayer = 1) {
        for (let i = 0; i < numLayersAdded; i++) {
            let numOfLayers = this.layers.childElementCount;

            const layerGroup = document.createElement('li');
            layerGroup.classList.add('layer-group');

            const layerBar = document.createElement('div');
            layerBar.classList.add('layer-bar');

            const deleteLayerIcon = document.createElement('img');
            deleteLayerIcon.classList.add('delete-layer');
            deleteLayerIcon.setAttribute('src', 'https://via.placeholder.com/20');
            //TODO add functionality to delete layer

            const layerText = document.createElement('span');
            layerText.classList.add('layer-text');
            layerText.innerText = `Layer ${numOfLayers + 1}`;

            const dropDownIcon = document.createElement('img');
            dropDownIcon.classList.add('drop-down-button');
            dropDownIcon.setAttribute('src', 'https://via.placeholder.com/20');
            //TODO add functionality to drop down

            layerBar.appendChild(deleteLayerIcon);
            layerBar.appendChild(layerText);
            layerBar.appendChild(dropDownIcon);

            layerGroup.appendChild(layerBar);

            const nodeList = document.createElement('ol');
            nodeList.classList.add('node-list');

            const addNode = document.createElement('img');
            addNode.classList.add('add-node');
            addNode.src = 'https://via.placeholder.com/20';

            layerGroup.appendChild(nodeList);
            layerGroup.appendChild(addNode);

            this.addNode(layerGroup, numNodesInLayer);

            this.layers.appendChild(layerGroup);
        }
    };

    addNode(layer, numNodesAdded = 1) {
        for (let i = 0; i < numNodesAdded; i++) {
            const nodeLayer = layer.querySelector('.node-list');
            let numOfNodes = nodeLayer.childElementCount;

            const node = document.createElement('li');
            node.innerText = `Node ${numOfNodes + 1}`;

            nodeLayer.appendChild(node);

            if (numNodesAdded === 1) {
                return node;
            }
        }
    };

    removeLayer(layerIndex) {
        const layers = this.layers.children;
        layers[layerIndex].remove();

        for (let i = 0; i < layers.length; i++) {
            layers[i].querySelector('.layer-text').innerText = `Layer ${i + 1}`
        }
        return true;
    }

    removeNode(layer) {
        const layerNodes = layer.querySelector('.node-list');
        layerNodes.lastChild.remove();
    }
}