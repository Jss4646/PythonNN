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
    addNodeInformationInteraction();
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

function addNodeInformationInteraction() {

}
