// The gamesoup namespace.
var gamesoup = new Object();

(function() {

// Create objects in a namespace hierarchy, only if they have not been yet created.
gamesoup.namespace = function(namespace) {
    namespace.split('.').inject(window, function(parent, childName) {
        var child = parent[childName]
        if (Object.isUndefined(child)) {
            child = new Object();
            parent[childName] = child;
        }
        return child;
    });
}

gamesoup.gridSize = 20;

})();
