/**
 * Adds an event listener to the drop down icon to give it its functionality of expanding and retracting the node list
 *
 * @param {HTMLElement} dropdownIcon - the icon that you wish to give the event listener
 */
function addDropdownInteraction(dropdownIcon) {
    dropdownIcon.addEventListener('click', function(selectedIcon) {
        const layer = selectedIcon.path[2];
        const nodeList = layer.childNodes[1];
        const nodeControls = layer.childNodes[2];

        nodeList.classList.toggle('hidden-list');
        nodeControls.classList.toggle('hidden-list');
    });
}

/**
 * Add a event listener to the add layer icon to give it its functionality
 */
function addAddLayerInteraction() {
    const addLayerIcon = document.querySelector('.add-layer');
    addLayerIcon.addEventListener('click', function () {
        network.addLayer(1,3)
    });
}

addAddLayerInteraction();


/**
 * Adds an event listener to the delete layer icon to give it its functionality
 *
 * @param {HTMLElement} deleteLayerIcon
 */
function addDeleteLayerInteraction(deleteLayerIcon) {
    deleteLayerIcon.addEventListener('click', function(selectedIcon) {
        const title = selectedIcon.target.nextSibling;
        const index = Number(title.innerHTML.slice(-1)) - 1;

        network.removeLayer(index);
    })
}

/**
 * Add a event listener to the add node icon to give it its functionality
 *
 * @param {HTMLElement} addNodeIcon
 */
function addAddNodeFunctionality(addNodeIcon) {
    addNodeIcon.addEventListener('click', function (selectedIcon) {
        const title = selectedIcon.path[2].querySelector('.layer-text');
        const index = Number(title.innerHTML.slice(-1)) - 1;

        network.addNode(index);
    })
}

/**
 * Add a event listener to the delete node icon to give it its functionality
 *
 * @param {HTMLElement} deleteNodeIcon
 */
function addDeleteNodeInteraction(deleteNodeIcon) {
    deleteNodeIcon.addEventListener('click', function(selectedIcon) {
        const title = selectedIcon.path[2].querySelector('.layer-text');
        const index = Number(title.innerHTML.slice(-1)) - 1;

        network.removeNode(index);
    })
}
