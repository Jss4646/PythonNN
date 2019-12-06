/**
 * Adds hover and click detection to a node
 *
 * @param node
 */
function addNodeInteraction(node) {
    node.addEventListener('mouseenter', function (event) {
        event.target.classList.replace('no-hover', 'node-hover')
    });

    node.addEventListener('mouseleave', function (event) {
        event.target.classList.replace('node-hover', 'no-hover')
    });

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
