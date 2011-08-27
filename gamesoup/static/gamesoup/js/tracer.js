(function() {

function showObjectDetails(objectContainer) {
    var hashClass = ".object-container.hash-" + objectContainer.getAttribute('hash');
    var handles = $$(hashClass + " .handle");
    var visibleDetails = $$(hashClass + " .details.visible");
    if (visibleDetails.length > 0) {
        visibleDetails[0].dragRelease();
    } else {
        var details = objectContainer.down('.details');
        handles.invoke('addClassName', 'showing-details');
        details.addClassName('visible');
        details.setStyle({position: 'fixed'});
        details.show();
        var drag = new Draggable(details);
        details.dragRelease = function(details, drag) {
            handles.invoke('removeClassName', 'showing-details');
            drag.destroy();
            details.removeClassName('visible');
            details.setStyle({position: 'absolute'});
            details.hide();
        }.curry(details, drag);
    }
}

function showTracebackDetails(methodCall) {
    var tb = methodCall.down('.tb');
    var handle = methodCall.down('.header .method');
    if (tb.visible()) {
        tb.dragRelease();
    } else {
        handle.addClassName('showing-details');
        tb.setStyle({position: 'fixed'});
        tb.show();
        var drag = new Draggable(tb);
        tb.dragRelease = function(tb, drag) {
            handle.removeClassName('showing-details');
            drag.destroy();
            tb.setStyle({position: 'absolute'});
            tb.hide();
        }.curry(tb, drag);
    }
}

function clickRouter(event) {
    var node = event.target;
    var objectContainer = node.up('.object-container');
    var methodCall = node.up('.method-call');
    if (objectContainer) {
        if (node.hasClassName('handle')) showObjectDetails(objectContainer);
        if (node.hasClassName('close-button')) showObjectDetails(objectContainer);
    }
    else if (methodCall) {
        if (node.hasClassName('method')) showTracebackDetails(methodCall);
        if (node.hasClassName('close-button')) showTracebackDetails(methodCall);
    }
}

document.observe('dom:loaded', function() {
    $('trace').observe('click', clickRouter);
});
})();
