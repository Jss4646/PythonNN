/**
 * Adds hover and click detection to a node
 *
 * @param node
 */
function addNodeInteraction(node) {
    addHoverInteraction(node);
    addNodeClickInteraction(node);
}

function addHoverInteraction(htmlElement) {
    htmlElement.addEventListener('mouseenter', function (event) {
        event.target.classList.replace('no-hover', 'node-hover')
    });

    htmlElement.addEventListener('mouseleave', function (event) {
        event.target.classList.replace('node-hover', 'no-hover')
    });
}


function addNodeClickInteraction(node) {
    addNodeEventlistenerInteraction(node);
    addNodeInformationInteraction(node);
}

function addNodeEventlistenerInteraction(node) {
    node.addEventListener('click', function (event) {

        event.target.classList.replace('node-hover', 'node-selected');

        const nodes = document.querySelectorAll('.node');

        nodes.forEach(function (node) {
            if (node !== event.target && node.classList.contains('node-selected')) {
                node.classList.replace('node-selected', 'no-hover');
            }
        })
    });
}

function addNodeInformationInteraction(node) {
    node.addEventListener('click', function (event) {
        let node = event.target;
        let layerNodes = node.parentNode;
        let layer = layerNodes.parentNode;
        let network = layer.parentNode;

        let layerList = Array.from(layerNodes.children);
        let networkList = Array.from(network.children);

        let nodeIndex = layerList.indexOf(node);
        let layerIndex = networkList.indexOf(layer);
        let indexs = {
            'layerIndex': layerIndex,
            'nodeIndex': nodeIndex,
        };

        socket.emit('send node data', indexs);
        socket.on('neuron data', function (data) {
            let weightsElement = document.querySelector('.weights ol');
            let weightElementList = Array.from(weightsElement.children);

            let biasElement = document.querySelector('.bias ol');

            if (Array.from(biasElement.children).length === 1) {
                biasElement.children[0].remove()
            }

            let biasSingleElement = document.createElement('li');
            let bias = data.bias;
            let decimalPoints = 10 ** 5;
            biasSingleElement.innerText = `${Math.round(bias * decimalPoints) / decimalPoints}`;

            biasElement.append(biasSingleElement);

            let weightsLength = data.weights.length;

            weightElementList.forEach(function(weight) {
                weight.remove()
            });

            for (let i = 0; i < weightsLength; i++) {
                let weightElement = document.createElement('li');
                let weight = data.weights[i];
                let decimalPoints = 10 ** 5;

                weightElement.innerText = `${Math.round(weight * decimalPoints) / decimalPoints}`;
                weightsElement.append(weightElement);
            }
        })
    })
}
