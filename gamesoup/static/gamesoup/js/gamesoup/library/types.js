(function() {
gamesoup.namespace('gamesoup.library.types');

var gs = gamesoup;
var mod = gamesoup.library.types;

mod.BaseType = Class.create({
    initialize: function(id) {
        this._id = id;
    },
    createDOM: function() {
        this._node = new Element('div', {id: this._id});
        return this._node;
    },
    isVisible: function() {
        return false;
    },
    isStateful: function() {
        return false;
    },
    register: function() {
        // Does nothing. Override to provide custom registration.
    },
    unregister: function() {
        // Does nothing. Override to provide custom take-down.
    },
    observe: function(eventName, action) {
        this._node.observe(eventName, action);
    },
    stopObserving: function(eventName, action) {
        this._node.stopObserving(eventName, action);
    },
    getNode: function() {
        return this._node;
    },
    getIdentifier: function() {
        return this._id;
    }
});

})();
