
const layers = document.querySelector('.layers');

function network() {

    this.addLayer = function (addNumOfLayers) {

        for (let i = 0; i < addNumOfLayers; i++) {
            let numOfLayers = layers.childElementCount;

            const layer = document.createElement('div');
            layer.id = `layer-${numOfLayers + 1}-viewport`;

            const title = document.createElement('h2');
            title.innerText = `Layer ${numOfLayers + 1}`;
            layer.appendChild(title);

            const nodes = document.createElement('div');
            nodes.classList.add('layer-nodes');
            this.addNode(nodes, 1);

            layers.appendChild(layer);
        }

    };

    this.addNode = function (layerNodeDiv, addNumOfNodes, numOfLayers) {
        const node = document.createElement('div');
        node.classList.add('node sigmoid-node no-hover')
        node.id = ``
    };

    this.removeLayer = function () {

    };

    this.removeNode = function () {

    };
}

const nn = new network();
nn.addLayer(1);