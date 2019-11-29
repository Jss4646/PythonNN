/**
 * Adds hover and click detection to a node
 *
 * @param node
 */
function addNodeInteraction(node) {
    node.addEventListener('mouseenter', function (selected_node) {
        selected_node.target.classList.replace('no-hover', 'node-hover')
    });

    node.addEventListener('mouseleave', function (selected_node) {
        selected_node.target.classList.replace('node-hover', 'no-hover')
    });

    node.addEventListener('click', function (selected_node) {

        selected_node.target.classList.replace('node-hover', 'node-selected');

        const nodes = document.querySelectorAll('.node');

        nodes.forEach(function (node) {
            if (node !== selected_node.target && node.classList.contains('node-selected')) {
                node.classList.replace('node-selected', 'no-hover');
            }
        })
    });
}
